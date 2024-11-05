### 2D ISING MODEL ###

def ising2d6(size, temps, frames, iters, interval=10):
    
    import random
    from matplotlib import pyplot as plt, animation
    from math import exp

    def generate(size):
        spins = [[1 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if random.random()<0.5:
                    spins[i][j] = -1
        return spins

    def energy(n1, n2, s):
        n = len(s)
        return 2*s[n1%n][n2%n]*(s[(n1+1)%n][n2%n]+s[(n1-1)%n][n2%n]+
                        s[n1%n][(n2+1)%n]+s[n1%n][(n2-1)%n])
    
    def init():
        for i in range(6):
            ims[i].set_data(spins[i])
        return ims

    def step(kk):
        for k in range(6):
            for _ in range(iters):
                i = random.randrange(size)
                j = random.randrange(size)
                de = energy(i, j, spins[k])
                if de<=0:
                    spins[k][i][j] *= -1
                elif random.random()<energies[k][de]:
                    spins[k][i][j] *= -1
        for i in range(6):
            ims[i].set_data(spins[i])
        return ims

    keys = list(range(-8, 9, 4))
    values = [[exp(-i/temp) for i in keys] for temp in temps]
    energies = []
    for i in range(6):
        d = {}
        for j in range(len(keys)):
            d[keys[j]] = values[i][j]
        energies.append(d)
    spins = [generate(size) for i in range(6)]
    
    fig, ax = plt.subplots(2, 3, figsize=(12, 8), facecolor='white')
    temps_ = [[temps[i] for i in range(3)], [temps[i] for i in range(3, 6)]]
    ims = [None]*6
    
    k = 0
    for i in range(2):
        for j in range(3):
            ax[i, j].set_xlim(0, size)
            ax[i, j].set_ylim(0, size)
            ax[i, j].set_title(fr'$T = {temps_[i][j]}$', size=20)
            ax[i, j].axis('off')
            ims[k] = ax[i, j].imshow(spins[k], cmap='gray')
            k += 1
                
    anim = animation.FuncAnimation(fig=fig, func=step, frames=frames, init_func=init, interval=interval)
    
    anim.save(f'ising2d6_{temps}.mp4')
    plt.close(fig)
    print('Animation is saved.')
    
    return

###

ising2d6(size=100, temps=(1, 1.5, 2, 2.5, 3, 5), frames=2000, iters=200)