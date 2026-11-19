import ex06
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(dpi=60)

ims = []


def play(program: list[int], controller: ex06.Controller) -> ex06.Game:
    """Play the game in `program` until it halts, asking `controller` for every input.

    Return the Game at the end.
    """
    computer = ex06.Computer(program)
    game = ex06.Game()
    game.update(computer.run([]))

    while not computer.halted:
        ims.append([ax.imshow(ex06.screen_rows(game), "Purples")])
        game.update(computer.run([controller.choose(game)]))

    return game


program = ex06.load_program(ex06.PROGRAM_FILE)
game = ex06.Game()
game = play(program, ex06.Autopilot())

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)

writer = animation.PillowWriter(fps=20)
ani.save("students/jay-temme/ex06/animation.gif", writer=writer)

plt.show()
