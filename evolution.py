"""Ouroboros Loop - Evolution Engine (debuggable)."""
import sys, os, tempfile, subprocess, time, random
sys.path.insert(0, '.')
from safe_lib import SafeOS
from sovereign_ai import SovereignAI, Niat

class EvolutionEngine:
    def __init__(self, sovereign_ai):
        self.ai = sovereign_ai
        self.generations_log = []

    def evolve(self, niat_str, expected_output, input_data="", generations=5, timeout=5):
        print(f"\n[EVOLVE] Niat: {niat_str}")
        print(f"         Target output: '{expected_output}'")
        print(f"         Input data: '{input_data}'")

        kode, review = self.ai.ciptakan(niat_str)
        best_code = kode
        best_score = self._evaluate(kode, expected_output, input_data, timeout, debug=True)

        history = [{'generation': 0, 'score': best_score, 'code': best_code}]

        for gen in range(1, generations + 1):
            mutated = self._mutate(best_code)
            score = self._evaluate(mutated, expected_output, input_data, timeout)
            if score > best_score:
                best_code = mutated
                best_score = score
                print(f"  Gen {gen}: skor naik -> {best_score:.2f}")
            else:
                print(f"  Gen {gen}: skor tetap {score:.2f}")
            history.append({'generation': gen, 'score': score, 'code': mutated})

        if best_score > 0.7:
            from knowledge import KnowledgeBase
            kb = KnowledgeBase()
            anchors = self.ai.ouroboros.anchor(best_code)
            hasil_review = self.ai.review(best_code)
            kb.learn_from_code(best_code, 'python', anchors, hasil_review.get('voids', []))
            kb.save()
            print("  [+] Pola baru disimpan ke KnowledgeBase")

        return {
            'best_code': best_code,
            'best_score': best_score,
            'history': history
        }

    def _evaluate(self, code, expected_output, input_data, timeout, debug=False):
        # Security score dari Ouroboros
        review = self.ai.review(code)
        security_score = review['skor_keamanan']

        # Eksekusi kode
        exec_score = 0.0
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write(code)
                tmp.flush()
                tmp_path = tmp.name

            proc = subprocess.run(
                [sys.executable, tmp_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if debug:
                print(f"    [DEBUG] returncode: {proc.returncode}")
                print(f"    [DEBUG] stdout: '{proc.stdout.strip()}'")
                print(f"    [DEBUG] stderr: '{proc.stderr.strip()}'")

            os.unlink(tmp_path)

            if proc.returncode == 0 and proc.stderr.strip() == '':
                output = proc.stdout.strip()
                if output == expected_output.strip():
                    exec_score = 1.0
                else:
                    # Kemiripan string
                    exec_score = self._similarity(output, expected_output)
            else:
                exec_score = 0.0
        except subprocess.TimeoutExpired:
            if debug:
                print("    [DEBUG] Timeout expired")
            exec_score = 0.0
            try:
                os.unlink(tmp_path)
            except:
                pass
        except Exception as e:
            if debug:
                print(f"    [DEBUG] Exception: {e}")
            exec_score = 0.0
            try:
                os.unlink(tmp_path)
            except:
                pass

        total_score = 0.4 * security_score + 0.6 * exec_score
        if debug:
            print(f"    [DEBUG] security={security_score:.2f}, exec={exec_score:.2f}, total={total_score:.2f}")
        return total_score

    def _similarity(self, a, b):
        if not a or not b:
            return 0.0
        min_len = min(len(a), len(b))
        matches = sum(1 for i in range(min_len) if a[i] == b[i])
        return matches / max(len(a), len(b))

    def _mutate(self, code):
        lines = code.split('\n')
        if not lines:
            return code
        mutation_type = random.choice(['rename_var', 'change_comment', 'add_whitespace'])
        if mutation_type == 'rename_var' and len(lines) > 2:
            line_idx = random.randint(0, len(lines)-1)
            if '=' in lines[line_idx]:
                lines[line_idx] = lines[line_idx].replace('x', '_x')
        elif mutation_type == 'change_comment':
            line_idx = random.randint(0, len(lines)-1)
            if not lines[line_idx].strip().startswith('#'):
                lines[line_idx] = '# ' + lines[line_idx]
            else:
                lines[line_idx] = lines[line_idx].replace('# ', '# [mutated] ')
        elif mutation_type == 'add_whitespace':
            idx = random.randint(0, len(lines))
            lines.insert(idx, '')
        return '\n'.join(lines)
