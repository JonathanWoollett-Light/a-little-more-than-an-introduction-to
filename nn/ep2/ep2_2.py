from manim import *
from ecommon import (
    get_title_screen,
    SCENE_WAIT,
    get_equations,
    get_highlight_box,
    rescale,
    retainTransform,
)

# Convolutional foreprop
class ep2_2(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.2, "Convolutional forepropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_equations(self, spacing=0.1):
        side_equations = get_equations(
            equations=[
                r"a^{l+1} = A(z^l)",
                r"z^l = w^l a^l + b^l",
                r"z^l_{i,j} = (a^l * w^l)_{i,j} + b^l",  #
            ],
            scale=0.5,
        )  #

        title = Text("Convolutional Foreprop")
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

    def play_foreprop(
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

        j2 = Matrix([1, 1], h_buff=h_buff).set_color(GREY)
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

        base_starting = starting.copy()

        self.play(Write(base_starting))
        self.wait()

        everything.shift(2.2 * UP)
        self.play(Transform(base_starting, starting))
        everything.shift(2 * LEFT)
        self.play(ReplacementTransform(base_starting, starting))

        # Equation highlights
        a = get_highlight_box(side_equations[0][0])
        dense_z = get_highlight_box(side_equations[0][1])
        conv_z = get_highlight_box(side_equations[0][2])

        self.play(Write(conv_z))

        # element_size = (image.get_width()/image_size[0],image.get_height()/image_size[1])
        # shift = (temp.get_width()/2-element_size[0]/2,-temp.get_height()/2+element_size[1]/2,0)

        # z1
        # ----------------------------
        a1_highlight = get_highlight_box(a1, buffer=0.1)
        self.play(Write(a1_highlight))

        f11_highlight = get_highlight_box(f1[0], buffer=0.1)
        self.play(Write(f11_highlight))
        b11_highlight = get_highlight_box(b1[0], buffer=0.1)
        self.play(Write(b11_highlight))
        z11_highlight = get_highlight_box(z1[0], buffer=0.1)
        self.play(Write(z11_highlight))

        j1 = Matrix([[1, 1], [1, 1]], h_buff=h_buff).set_color(GREY)
        j1.scale(scale)

        calculation = VGroup(
            a1.copy(),
            MathTex("*"),
            f1[0].copy(),
            MathTex("+"),
            b1[0].copy(),
            j1,
            MathTex("="),
            z1[0].copy(),
        )
        calculation.arrange()

        if (
            calculation.get_x() - calculation.get_width() / 2
            < side_equations.get_x() + side_equations.get_width() / 2
        ):
            calculation.move_to(
                [
                    side_equations.get_x()
                    + side_equations.get_width() / 2
                    + calculation.get_width() / 2
                    + buff,
                    calculation.get_y(),
                    calculation.get_z(),
                ]
            )

        self.play(
            Write(calculation[1]),
            Write(calculation[3]),
            Write(calculation[5]),
            Write(calculation[6]),
            Write(calculation[7][1:3]),
        )
        self.play(ReplacementTransform(a1.copy(), calculation[0]))
        self.play(ReplacementTransform(f1[0].copy(), calculation[2]))
        self.play(ReplacementTransform(b1[0].copy(), calculation[4]))
        self.play(Write(calculation[7][0]))
        self.play(ReplacementTransform(calculation[7].copy(), z1[0]))

        self.play(
            Uncreate(calculation[2][0]),
            Uncreate(calculation[4][0]),
            Uncreate(calculation[7][0]),
        )

        f12_highlight = get_highlight_box(f1[1], buffer=0.1)
        b12_highlight = get_highlight_box(b1[1], buffer=0.1)
        z12_highlight = get_highlight_box(z1[1], buffer=0.1)
        self.play(
            ReplacementTransform(f11_highlight, f12_highlight),
            ReplacementTransform(b11_highlight, b12_highlight),
            ReplacementTransform(z11_highlight, z12_highlight),
        )

        f12copy = f1[1].copy()
        f12copy.move_to(calculation[2])
        self.play(ReplacementTransform(f1[1].copy(), f12copy))

        b12copy = b1[1].copy()
        b12copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b1[1].copy(), b12copy))

        z12copy = z1[1].copy()
        z12copy.move_to(calculation[7].get_center())
        self.play(Write(z12copy))
        self.play(ReplacementTransform(z12copy.copy(), z1[1]))

        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(calculation[2][1:3]),
            Uncreate(f12copy),
            Uncreate(calculation[3]),
            Uncreate(calculation[4][1:3]),
            Uncreate(b12copy),
            Uncreate(calculation[5]),
            Uncreate(calculation[6]),
            Uncreate(calculation[7][1:3]),
            Uncreate(z12copy),
        )
        self.play(Uncreate(b12_highlight), Uncreate(f12_highlight))

        # a2
        # ----------------------------

        z1_highlight = get_highlight_box(z1, buffer=0.1)
        a2_highlight = get_highlight_box(a2, buffer=0.1)
        self.play(
            ReplacementTransform(a1_highlight, z1_highlight),
            ReplacementTransform(z12_highlight, a2_highlight),
        )

        conv_z = retainTransform(self, conv_z, a)

        calculation = VGroup(MathTex("A ("), z1.copy(), MathTex(")="), a2.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][0][1:3]),
            Write(calculation[3][1][1:3]),
        )
        self.play(ReplacementTransform(z1.copy(), calculation[1]))
        self.play(Write(calculation[3][0][0]), Write(calculation[3][1][0]))
        self.play(ReplacementTransform(calculation[3].copy(), a2))
        self.play(Uncreate(calculation))

        # z2
        # ----------------------------

        a = retainTransform(self, a, conv_z)

        z21_highlight = get_highlight_box(z2[0], buffer=0.1)

        self.play(
            Transform(z1_highlight, a2_highlight),
            ReplacementTransform(a2_highlight, z21_highlight),
        )

        f21_highlight = get_highlight_box(f2[0], buffer=0.1)
        b21_highlight = get_highlight_box(b2[0], buffer=0.1)
        self.play(Write(f21_highlight), Write(b21_highlight))

        j2 = Matrix([1, 1], h_buff=h_buff).set_color(GREY)
        j2.scale(scale)

        calculation = VGroup(
            a2.copy(),
            MathTex("*"),
            f2[0].copy(),
            MathTex("+"),
            b2[0].copy(),
            j2,
            MathTex("="),
            z2[0].copy(),
        )
        calculation.arrange()

        if (
            calculation.get_x() - calculation.get_width() / 2
            < side_equations.get_x() + side_equations.get_width() / 2
        ):
            calculation.move_to(
                [
                    side_equations.get_x()
                    + side_equations.get_width() / 2
                    + calculation.get_width() / 2
                    + buff,
                    calculation.get_y(),
                    calculation.get_z(),
                ]
            )

        self.play(
            Write(calculation[1]),
            Write(calculation[3]),
            Write(calculation[5]),
            Write(calculation[6]),
            Write(calculation[7][1:3]),
        )
        self.play(ReplacementTransform(a2.copy(), calculation[0]))
        self.play(ReplacementTransform(f2[0].copy(), calculation[2]))
        self.play(ReplacementTransform(b2[0].copy(), calculation[4]))
        self.play(Write(calculation[7][0]))
        self.play(ReplacementTransform(calculation[7].copy(), z2[0]))

        self.play(
            Uncreate(calculation[2][0][0]),
            Uncreate(calculation[2][1][0]),
            Uncreate(calculation[4][0]),
            Uncreate(calculation[7][0]),
        )

        f22_highlight = get_highlight_box(f2[1], buffer=0.1)
        b22_highlight = get_highlight_box(b2[1], buffer=0.1)
        z22_highlight = get_highlight_box(z2[1], buffer=0.1)
        self.play(
            ReplacementTransform(f21_highlight, f22_highlight),
            ReplacementTransform(b21_highlight, b22_highlight),
            ReplacementTransform(z21_highlight, z22_highlight),
        )

        f22copy = f2[1].copy()
        f22copy.move_to(calculation[2])
        self.play(ReplacementTransform(f2[1].copy(), f22copy))

        b22copy = b2[1].copy()
        b22copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b2[1].copy(), b22copy))

        z22copy = z2[1].copy()
        z22copy.move_to(calculation[7].get_center())
        self.play(Write(z22copy[0]))
        self.play(ReplacementTransform(z22copy.copy(), z2[1]))

        self.play(Uncreate(f22copy), Uncreate(b22copy), Uncreate(z22copy[0]))

        f23_highlight = get_highlight_box(f2[2], buffer=0.1)
        b23_highlight = get_highlight_box(b2[2], buffer=0.1)
        z23_highlight = get_highlight_box(z2[2], buffer=0.1)
        self.play(
            ReplacementTransform(f22_highlight, f23_highlight),
            ReplacementTransform(b22_highlight, b23_highlight),
            ReplacementTransform(z22_highlight, z23_highlight),
        )

        f23copy = f2[2].copy()
        f23copy.move_to(calculation[2])
        self.play(ReplacementTransform(f2[2].copy(), f23copy))

        b23copy = b2[2].copy()
        b23copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b2[2].copy(), b23copy))

        z23copy = z2[2].copy()
        z23copy.move_to(calculation[7].get_center())
        self.play(Write(z23copy))
        self.play(ReplacementTransform(z23copy.copy(), z2[2]))

        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(calculation[2][0][1:3]),
            Uncreate(calculation[2][1][1:3]),
            Uncreate(f23copy),
            Uncreate(calculation[3]),
            Uncreate(calculation[4][1:3]),
            Uncreate(calculation[5]),
            Uncreate(b23copy),
            Uncreate(calculation[6]),
            Uncreate(calculation[7][1:3]),
            Uncreate(z23copy),
        )

        self.play(Uncreate(b23_highlight), Uncreate(f23_highlight))

        # a3
        # ----------------------------

        z2_highlight = get_highlight_box(z2, buffer=0.1)
        a3_highlight = get_highlight_box(a3, buffer=0.1)
        self.play(
            ReplacementTransform(z1_highlight, z2_highlight),
            ReplacementTransform(z23_highlight, a3_highlight),
        )

        conv_z = retainTransform(self, conv_z, a)

        calculation = VGroup(MathTex("A ("), z2.copy(), MathTex(")="), a3.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][0][1:3]),
            Write(calculation[3][1][1:3]),
            Write(calculation[3][2][1:3]),
        )
        self.play(ReplacementTransform(z2.copy(), calculation[1]))
        self.play(
            Write(calculation[3][0][0]),
            Write(calculation[3][1][0]),
            Write(calculation[3][2][0]),
        )
        self.play(ReplacementTransform(calculation[3].copy(), a3))
        self.play(Uncreate(calculation))

        # z3
        # ----------------------------

        z3_highlight = get_highlight_box(z3, buffer=0.1)

        w1_highlight = get_highlight_box(w1, buffer=0.1)
        b3_highlight = get_highlight_box(b3, buffer=0.1)

        self.play(
            Transform(z2_highlight, a3_highlight),
            ReplacementTransform(a3_highlight, z3_highlight),
        )
        self.play(Write(w1_highlight), Write(b3_highlight))

        a = retainTransform(self, a, dense_z)

        flat = VGroup(a3[0].copy(), a3[1].copy(), a3[2].copy())
        flat.arrange(DOWN, buff=0.05)

        calculation = VGroup(
            w1.copy(), flat, MathTex("+"), b3.copy(), MathTex("="), z3.copy()
        )
        calculation.arrange()

        flattened = Matrix([2, 1, 3, 2, 5, 3], h_buff=h_buff)
        flattened.scale(scale)
        flattened.move_to(flat.get_center())

        self.play(
            Write(calculation[2]), Write(calculation[4]), Write(calculation[5][1:3])
        )

        self.play(ReplacementTransform(a3[0].copy(), flat[0]))
        self.play(ReplacementTransform(a3[1].copy(), flat[1]))
        self.play(ReplacementTransform(a3[2].copy(), flat[2]))
        l_brackets = VGroup(flat[0][1], flat[1][1], flat[2][1])
        r_brackets = VGroup(flat[0][2], flat[1][2], flat[2][2])
        self.play(
            ReplacementTransform(l_brackets, flattened[1]),
            ReplacementTransform(r_brackets, flattened[2]),
        )

        self.play(
            ReplacementTransform(w1.copy(), calculation[0]),
            ReplacementTransform(b3.copy(), calculation[3]),
        )

        self.play(Write(calculation[5][0]))
        self.play(ReplacementTransform(calculation[5].copy(), z3))
        self.play(
            Uncreate(calculation[0]),
            Uncreate(flattened[1:3]),
            Uncreate(flat[0][0]),
            Uncreate(flat[1][0]),
            Uncreate(flat[2][0]),
            Uncreate(calculation[2:6]),
        )
        self.play(Uncreate(w1_highlight), Uncreate(b3_highlight))

        # a3
        # ----------------------------

        a4_highlight = get_highlight_box(a4, buffer=0.1)
        self.play(
            Transform(z2_highlight, z3_highlight),
            ReplacementTransform(z3_highlight, a4_highlight),
        )

        dense_z = retainTransform(self, dense_z, a)

        calculation = VGroup(MathTex("A ("), z3.copy(), MathTex(")="), a4.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]), Write(calculation[2]), Write(calculation[3][1:3])
        )
        self.play(ReplacementTransform(z3.copy(), calculation[1]))
        self.play(Write(calculation[3][0]))
        self.play(ReplacementTransform(calculation[3].copy(), a4))

    def construct(self):
        self.play_intro()

        title, side_equations = self.play_equations()

        self.play_net(side_equations)

        self.play_foreprop(side_equations)
        self.wait(3)
