from ecommon import (
    get_equations,
    get_explicit_conv_net,
    get_highlight_box,
    get_title_screen,
    rescale,
    retainTransform,
    setup,
)
from manim import *


# Convolutional backprop
class EpisodeScene(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.3, "Convolutional backpropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_equations(self, spacing=0.1):
        side_equations = get_equations(
            equations=[
                r"a^{l+1} = A(z^l)",
                r"z^l = w^l a^l + b^l",
                r"\delta^L = \nabla_a C \odot A'(z^L)",
                r"\delta^l = a",
                r"\frac{\partial C}{\partial b^l} = \delta^l",
                r"\frac{\partial C}{\partial w^l_{m,n}} = \delta_l \odot \frac{\partial z^l}{\partial w^l}",  #
            ],
            wheres=[r"\delta_l = \frac{\partial C}{\partial z^l}"],
            scale=0.5,
        )  #

        title = Text("Convolutional Backprop")
        title.move_to(side_equations.get_center() + 3.3 * UP)

        self.play(Write(title))
        self.wait(3)
        self.play(Write(side_equations))
        self.wait(3)
        self.play(Transform(side_equations, side_equations.copy().shift(5 * LEFT)))
        self.play(Transform(side_equations, side_equations.copy().shift(0.2 * DOWN)))

        return (title, side_equations)

    def play_net(self, side_equations, spacing=0.1):
        net = get_explicit_conv_net((3, 3), [(2, 2, 2), (3, 1, 2)], [3])
        net.move_to(
            [
                side_equations.get_x()
                + side_equations.get_width() / 2
                + net.get_width() / 2
                + spacing,
                net.get_y(),
                0,
            ]
        )
        self.play(Write(net))
        self.wait(3)
        self.play(ReplacementTransform(net, net.copy().shift(DOWN * 2)))

    def play_backprop(
        self, side_equations, spacing=0.1, h_buff=0.5, scale=0.4, buff=0.5
    ):
        (
            a1,
            f1,
            b1,
            z1,
            a2,
            f2,
            b2,
            z2,
            a3,
            w1,
            b3,
            z3,
            a4,
            everything,
            starting,
        ) = setup(scale=scale, h_buff=h_buff)

        j2 = Matrix([[1], [1]], h_buff=h_buff).set_color(GREY)
        j2.scale(scale)

        everything.move_to(
            [
                side_equations.get_x()
                + side_equations.get_width() / 2
                + everything.get_width() / 2
                + spacing,
                everything.get_y(),
                0,
            ]
        )

        self.play(Write(everything))
        self.wait()

    def construct(self):
        self.play_intro()

        title, side_equations = self.play_equations()

        self.play_net(side_equations)

        self.play_backprop(side_equations)
        self.wait(3)
