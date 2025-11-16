#Task_01

with open ("inp1.txt", "r") as f:
    pool = list(map(str, f.readline().strip().split(',')))
    target = "".join(f.readline().strip().split())
    std_id = list(map(int, f.readline().strip().split()))


if len(std_id) <= len(target):
    w = [1]
else:
    w = std_id[-len(target):]

def utility(gene, target, w):
    N = max(len(gene), len(target))
    utility = 0

    for i in range(N):
        if i < len(gene):
            gene_char = ord(gene[i])
        else:
            gene_char = 0
            
        if i < len(target):
            target_char = ord(target[i])
        else:
            target_char = 0

        if i < len(w):
            weight = w[i]
        else:
            weight = 1

        utility += weight * (gene_char - target_char)

    return -utility

def minimax(gene, pool, flag, alpha, beta):
    if not pool:
        return utility(gene, target, w), gene

    if flag:
        max_eval = float('-inf')
        best_seq = ""
        for i in range(len(pool)):
            new = gene + pool[i]
            new_pool = pool[:i] + pool[i+1:]
            eval, best = minimax(new, new_pool, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_seq = best
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return max_eval, best_seq
    else:
        min_eval = float('inf')
        best_seq = ""
        for i in range(len(pool)):
            new = gene + pool[i]
            new_pool = pool[:i] + pool[i+1:]
            eval, best = minimax(new, new_pool, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_seq = best
            beta = min(beta, eval)
            if alpha >= beta:
                break

        return min_eval, best_seq

gene = ""
score, best_seq = minimax(gene, pool, True, float('-inf'), float('inf'))

with open("output1.txt", "w") as f:
    f.write(f"Best gene sequence generated: {best_seq}\n")
    f.write(f"Utility score: {score}")



#Task_02

with open ("inp2.txt", "r") as f:
    pool = list(map(str, f.readline().strip().split(',')))
    target = "".join(f.readline().strip().split())
    std_id = list(map(int, f.readline().strip().split()))


if len(std_id) <= len(target):
    w = [1]
else:
    w = std_id[-len(target):]

booster = (std_id[0] * 10 + std_id[1]) / 100

def utility(gene, target, w):
    N = max(len(gene), len(target))
    utility = 0

    for i in range(N):
        if i < len(gene):
            gene_char = ord(gene[i])
        else:
            gene_char = 0

        if i < len(target):
            target_char = ord(target[i])
        else:
            target_char = 0

        if i < len(w):
            weight = w[i]
        else:
            weight = 1

        utility += weight * abs(gene_char - target_char)

    return -utility

def utility_with_S(gene, target, w, booster):
    N = max(len(gene), len(target))
    utility = 0

    s_index = -1
    for i in range(len(gene)):
        if gene[i] == 'S':
            s_index = i
            break

    for i in range(N):
        if i < len(gene):
            gene_char = ord(gene[i])
        else:
            gene_char = 0

        if i < len(target):
            target_char = ord(target[i])
        else:
            target_char = 0

        if s_index != -1 and i >= s_index:
            if i < len(w):
                weight = w[i] * booster
            else:
                weight = 1 * booster
        else:
            if i < len(w):
                weight = w[i] * len(target)
            else:
                weight = 1

        utility += weight * abs(gene_char - target_char)

    return -utility

def minimax(gene, pool, flag, alpha, beta):
    if not pool:
        if 'S' in gene:
            return utility_with_S(gene, target, w, booster), gene
        else:
            return utility(gene, target, w), gene
        
    if flag:
        max_eval = float('-inf')
        best_seq = ""
        for i in range(len(pool)):
            new = gene + pool[i]
            new_pool = pool[:i] + pool[i+1:]
            eval, best = minimax(new, new_pool, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_seq = best
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return max_eval, best_seq
    else:
        min_eval = float('inf')
        best_seq = ""
        for i in range(len(pool)):
            new = gene + pool[i]
            new_pool = pool[:i] + pool[i+1:]
            eval, best = minimax(new, new_pool, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_seq = best
            beta = min(beta, eval)
            if alpha >= beta:
                break

        return min_eval, best_seq

gene = ""
score, best_gene = minimax(gene, pool, True, float('-inf'), float('inf'))


with open("output2.txt", "w") as f:
    if 'S' in best_gene:
        f.write("Yes\nWith special nucleotide\n")
    else:
        f.write("No\nWith special nucleotide\n")
    f.write(f"Best gene sequence generated: {best_gene}\n")
    f.write(f"Utility score: {round(score, 2)}\n")


