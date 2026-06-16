import numpy as np
from sympy import Matrix, symbols

def generate_pricing_problem(student_id):
    
    seed = int(student_id)
    rng = np.random.default_rng(seed)

    # 生成 S
    S = int(rng.integers(2, 11))

    # 生成 K，满足 |S-K|<4
    k_low = max(2, S - 3)
    k_high = min(10, S + 3)
    K = int(rng.integers(k_low, k_high + 1))

    
    X = rng.integers(0, 100, size=(S, K))
    x0 = rng.integers(-1, 25, size=(K, 1))

    # 避免出现全零矩阵或全零价格
    if np.all(X == 0):
        X[0, 0] = 1
    if np.all(x0 == 0):
        x0[0, 0] = 1

    return {
        "student_id": seed,
        "seed": seed,
        "S": S,
        "K": K,
        "X": X,
        "x0": x0
    }


def print_pricing_problem(problem):
    """
    以适合作业发布的形式打印题目
    """
    print(f"student_id = {problem['student_id']}")
    print(f"S = {problem['S']}, K = {problem['K']}")
    print("X =")
    print(problem["X"])
    print("x0^T =")
    print(problem["x0"].T)


problem=generate_pricing_problem(23012006)
print_pricing_problem(problem)
X=problem["X"].T
x0=problem["x0"]
print(X.shape,x0.shape)
eq=np.concatenate((X, x0),axis=1)
print(eq)


rank_X = np.linalg.matrix_rank(X)
rank_eq = np.linalg.matrix_rank(eq)
print(rank_X,rank_eq)

if rank_X < rank_eq:
    print("该市场阿罗证券小于资产数,无法定价")
elif rank_X == X.shape[1]:
    print("该市场阿罗证券价格存在唯一解")
    lambdaa=np.linalg.lstsq(X, x0, rcond=None)
    print(lambdaa[0])
else:
    print("该市场阿罗证券的价格存在无穷多解")
    A_sym = Matrix(X)
    B_sym = Matrix(x0)
    from sympy import linsolve
    xs = symbols(f'x0:{A_sym.cols}')   #生成未知数符号
    sol = linsolve((A_sym, B_sym), xs)

    print("系统的通解集合：")
    print(sol)

    # 3. 如果你想手动提取“特解 + 基础解系”
    # 求零空间的基 (Nullspace)
    basis = A_sym.nullspace()
    print("\n零空间的基向量 (基础解系):")
    for i, v in enumerate(basis):
        print(f"zeta_{i + 1} = {v}")
    full_sol = list(sol)[0]
    # 2. 定义一个字典，将所有自由变量替换为 0
    # 我们可以遍历生成的符号 xs，如果它在结果中表现为“自己等于自己”，或者为了保险直接全设为 0
    special_params = {x: 0 for x in xs}
    # 3. 得到特解 (Particular Solution)
    particular_sol = full_sol.subs(special_params)
    print("\n提取的特解 (令自由变量为0):")
    print(particular_sol)


