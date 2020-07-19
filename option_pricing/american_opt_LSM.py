import numpy as np

def american_opt_LSM(S0, K, r, T, sigma, N, M, type):
# AmericanOptLSM - Price an american option via Longstaff-Schwartz Method
#
#   Returns the price of an American option computed using finite
#   difference method applied to the BlackScoles PDE.
#
#  Inputs:
#
#    S0      Initial asset price
#    K       Strike Price
#    r       Interest rate
#    T       Time to maturity of option
#    sigma   Volatility of underlying asset
#    N       Number of points in time grid to use (minimum is 3, default is 50)
#    M       Number of points in asset price grid to use (minimum is 3, default is 50)
#    type    True (default) for a put, false for a call

# if nargin < 6 || isempty(N), N = 50; elseif N < 3, error('N has to be at least 3'); end
# if nargin < 7 || isempty(M), M = 50; elseif M < 3, error('M has to be at least 3'); end
# if nargin < 8, type = true; end

    dt = T / N
    t = np.linspace(0, T, N + 1, endpoint=True)
    t = np.repeat(t.reshape(-1, 1), M, axis=1)

    R = np.exp((r - sigma**2 / 2) * dt + sigma * np.sqrt(dt) * np.random.normal(size=(N, M)))
    S = np.concatenate((S0 * np.ones((1, M)), R), axis=0)
    S = np.cumprod(S, axis=0)

    # ExTime = (M + 1) * np.ones((N, 1))

    # Now for the algorithm
    CF = np.zeros(S.shape) # Cash flow matrix

    CF[-1, :] = np.maximum(K - S[-1, :], np.zeros((1, M))) # Option only pays off if it is in the money

    for ii in np.arange(S.shape[0] - 2, 0, -1):
        if type:
            Idx = np.where(S[ii, :] < K) # Find paths that are in the money at time ii
        else:
            Idx = np.where(S[ii,:] > K) # Find paths that are in the money at time ii

        X = S[ii, Idx].transpose()
        X1 = X / S0

        Y = CF[ii + 1, Idx].transpose() * np.exp(-r * dt) # Discounted cashflow from ii + 1

        R = np.concatenate((np.ones(X1.shape), (1-X1), 1/2*(2-4*X1-X1**2)), axis=1)

        A = np.matmul(R.transpose(), R)
        b = np.matmul(R.transpose(), Y)
        a = np.linalg.solve(A, b) # Linear regression step

        C = np.matmul(R, a) # Cash flows as predicted by the model

        if type:
            Jdx = np.maximum(K - X, np.zeros(X.shape)) > C # Immediate exercise better than predicted cashflow
        else:
            Jdx = np.maximum(K - X, np.zeros(X.shape)) > C # Immediate exercise better than predicted cashflow

        nIdx = np.setdiff1d(np.linspace(1, M, M, endpoint=True), Idx[0][Jdx.transpose()[0]])

        CF[ii, Idx[Jdx]] = max(K - X[Jdx], 0)
        # ExTime[Idx[Jdx]] = ii
        CF[ii, nIdx] = np.exp(-r * dt) * CF[ii+1, nIdx]

    Price = np.mean(CF[2, :]) * np.exp(-r * dt)

    return Price

if __name__ == "__main__":
    S0 = 100
    K = 100
    r = 0.03
    T = 1
    sigma = 0.1
    N = 200
    M = 10000
    type = True
    price = american_opt_LSM(S0, K, r, T, sigma, N, M, type)
    print(price)