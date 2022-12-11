from manim import *
from ecommon import (
    get_title_screen,
    SCENE_WAIT,
    get_xor_net,
    get_equations,
    get_highlight_box,
    rescale,
    retainTransform,
)

# Batch backprop
class EpisodeScene(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.3, "Batch backpropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_equations(self):
        side_equations = get_equations(
            equations=[
                r"\delta^L = \nabla_a C \odot A'(z^L)",
                r"\delta^l = (w^{l+1})^T \delta^{l+1} \odot A'(z^l)",
                r"\frac{\partial C}{\partial b^l} = \delta^l J_n",
                r"\frac{\partial C}{\partial w^l} = \delta^l (a^l)^T",
            ],
            wheres=[
                r"\delta^l = \frac{\partial C}{\partial z^l}",
                r"J_n=[1_1,...,1_n]^T",
            ],
        )

        title = Text("Batch backpropagation")
        title.move_to(side_equations.get_center() + 3 * UP)

        self.play(Write(title))
        self.wait(3)
        self.play(Write(side_equations))
        self.wait(3)

        yield title
        yield side_equations

    def play_batch_backpropagation(
        self,
        title,
        side_equations,
        side_equation_scale=0.7,
        side_equation_space=0.1,
        store_scale=0.3,
        equation_scale=0.3,
        equation_buffer=0.1,
    ):

        # Sets up matricies with values
        # ----------------------------------------------------------
        a1 = Matrix([["0", "0", "1", "1"], ["0", "1", "0", "1"]], h_buff=0.6)
        a2 = Matrix(
            [
                ["0.42...", "0.47...", "0.37...", "0.42..."],
                ["0.57...", "0.62...", "0.59...", "0.64..."],
                ["0.64...", "0.52...", "0.75...", "0.64..."],
            ],
            h_buff=1.5,
        )
        a3 = Matrix(
            [
                ["0.53...", "0.62...", "0.65...", "0.63..."],
                ["0.63...", "0.53...", "0.54...", "0.54..."],
            ],
            h_buff=1.5,
        )

        z1 = Matrix(
            [
                ["-0.3", "-0.1", "-0.5", "-0.3"],
                ["0.3", "0.5", "0.4", "0.6"],
                ["0.6", "0.1", "1.1", "0.6"],
            ],
            h_buff=1.2,
        )
        z1e = Matrix(
            [
                ["-0.00...", "-0.01...", "0.00...", "0.00..."],
                ["0.01...", "0.00...", "0.02...", "-0.00..."],
                ["0.02...", "0.00...", "0.00...", "-0.01..."],
            ],
            h_buff=2,
        )
        z2 = Matrix(
            [
                ["0.55...", "0.49...", "0.61...", "0.56..."],
                ["0.15...", "0.12...", "0.18...", "0.16..."],
            ],
            h_buff=1.5,
        )
        z2e = Matrix(
            [
                ["0.12...", "0.14...", "-0.07...", "-0.08..."],
                ["0.15...", "-0.11...", "0.13...", "-0.1..."],
            ],
            h_buff=2,
        )

        w1 = Matrix([[-0.2, 0.2], [0.1, 0.2], [0.5, -0.5]]).set_color(RED)
        w1e = Matrix(
            [
                ["0.00...", "-0.00..."],
                ["0.01...", "-0.00..."],
                ["-0.01...", "-0.00..."],
            ],
            h_buff=2,
        ).set_color(GREEN)
        w2 = Matrix([[-0.2, 0.2, 0.5], [0.1, 0.2, 0.3]], h_buff=1).set_color(RED)
        w2e = Matrix(
            [["0.05...", "0.06...", "0.43..."], ["0.12...", "0.18...", "0.23..."]],
            h_buff=1.5,
        ).set_color(GREEN)

        b1 = Matrix([-0.3, 0.3, 0.6]).set_color(BLUE)
        b1e = Matrix(["-0.00...", "0.03...", "0.01..."]).set_color(GREEN)
        b2 = Matrix([0.2, -0.2]).set_color(BLUE)
        b2e = Matrix(["0.10...", "0.15..."]).set_color(GREEN)

        bu = Matrix([1, 1, 1, 1], h_buff=0.7)
        bu.scale(equation_scale)

        # Groups layer matricies
        n1 = VGroup(w1e, z1, b1, b1e, a2)
        n2 = VGroup(w2e, z2, b2, b2e, a3)

        # Sets side equation alignment
        new_side_equations = side_equations.copy()
        new_side_equations.scale(side_equation_scale)
        self.play(
            ReplacementTransform(
                side_equations,
                new_side_equations.copy().shift(5 * LEFT).shift(0.3 * DOWN),
            )
        )
        side_equations_alignment = (
            side_equations.get_x()
            + side_equations.get_width() / 2
            + side_equation_space
        )

        # Scales all matricies
        net_values_precise = VGroup(
            a1, w1, w1e, z1, b1, b1e, a2, w2, w2e, z2, b2, b2e, a3
        )
        net_values_precise.arrange(buff=0.3)
        net_values_precise.scale(store_scale)  # Scales down matricies
        net_values_precise.shift(2 * UP)

        # Shifts so it is visible
        net_values_precise.shift(4 * LEFT)

        # Sets highlight boxes
        # -----------------------------

        # Sets matrix highlight boxes
        n1Selected = get_highlight_box(n1, buffer=0.2)
        n2Selected = get_highlight_box(n2, buffer=0.2)

        # Sets equation highlight boxes
        outErrorEqSelected = get_highlight_box(side_equations[0][0])
        errorEqSelected = get_highlight_box(side_equations[0][1])
        bEqSelected = get_highlight_box(side_equations[0][2])
        wEqSelected = get_highlight_box(side_equations[0][3])

        # Sets net
        # -----------------------------

        mid_xor_net = get_xor_net(0.5, 0.25, 2)
        mid_xor_net.shift(2 * DOWN)

        # Sets output scene
        # ----------------------------------------------------------

        a3_scaled = a3.copy()
        a3_scaled.scale(1 / store_scale)
        a3_scaled.scale(equation_scale)
        a3_scaled.center()

        net_values_precise_excluding_errors = VGroup(
            a1, w1, w1e[1:3], z1, b1, b1e[1:3], a2, w2, w2e[1:3], z2, b2, b2e[1:3], a3
        )

        self.play(ReplacementTransform(title, title.copy().shift(0.5 * UP)))
        self.play(
            Write(net_values_precise_excluding_errors),
            Write(a3_scaled),
            Write(mid_xor_net),
        )
        self.wait(10)

        # Sets output error
        # ----------------------------------------------------------

        target = Matrix([["0", "0", "1", "1"], ["0", "1", "0", "1"]], h_buff=1)
        target.scale(equation_scale)

        z2e.scale(equation_scale)

        z2_scaled = z2.copy()
        z2_scaled.scale(1 / store_scale)
        z2_scaled.scale(equation_scale)

        # Sets calculation
        calculation = VGroup(
            z2e.copy(),
            MathTex("="),
            VGroup(a3_scaled.copy(), MathTex("-"), target),
            MathTex(r"\odot"),
            VGroup(MathTex(r"\sigma ' ("), z2_scaled.copy(), MathTex(r")")),
        )
        calculation[2].arrange(buff=equation_buffer)
        calculation[4].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        # Sets equation hightlight
        self.play(Write(outErrorEqSelected))

        # Sets other highlights
        mid_xor_net[0][2][0][0].set_color(YELLOW)
        mid_xor_net[0][2][1][0].set_color(YELLOW)
        mid_xor_net[1][1].set_color(YELLOW)
        self.play(
            Write(n2Selected),
            Write(mid_xor_net[0][2][0][0]),
            Write(mid_xor_net[0][2][1][0]),
            Write(mid_xor_net[1][1]),
        )

        self.play(ReplacementTransform(a3_scaled, calculation[2][0]))
        self.play(ReplacementTransform(z2.copy(), calculation[4][1]))

        # Writes calculation, avoiding rewriting transformed in matricies
        self.play(
            Write(calculation[0:2]),
            Write(calculation[2][1]),
            Write(calculation[2][2]),
            Write(calculation[3]),
            Write(calculation[4][0]),
            Write(calculation[4][2]),
        )
        self.wait()

        self.play(Uncreate(calculation[1:5]))

        # Sets output bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        outErrorEqSelected = retainTransform(self, outErrorEqSelected, bEqSelected)

        holder = calculation[0]  # Error holder

        b2e_scaled = b2e.copy()
        b2e_scaled.scale(1 / store_scale)
        b2e_scaled.scale(equation_scale)

        # Sets calculation
        calculation = VGroup(b2e_scaled, MathTex("="), z2e.copy(), bu.copy())
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        # Tranforms error into equation
        self.play(ReplacementTransform(holder, calculation[2]))

        self.wait()
        self.play(Write(calculation[0:2]), Write(calculation[3]))

        # Transforms result to bias error
        self.play(ReplacementTransform(calculation[0].copy(), b2e))

        # Uncreate calculation, sans error
        self.play(Uncreate(calculation[0:2]), Uncreate(calculation[3]))

        # Sets output weight error
        # ----------------------------------------------------------

        # Sets equation hightlight
        bEqSelected = retainTransform(self, bEqSelected, wEqSelected)

        w2e_scaled = w2e.copy()
        w2e_scaled.scale(1 / store_scale)
        w2e_scaled.scale(equation_scale)

        a2_scaled = a2.copy()
        a2_scaled.scale(1 / store_scale)
        a2_scaled.scale(equation_scale)

        holder = calculation[2]
        calculation = VGroup(
            w2e_scaled,
            MathTex("="),
            z2e.copy(),
            VGroup(MathTex(r"("), a2_scaled, MathTex(r")^T")),
        )
        calculation[3].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        # Tranforms error into calculation
        self.play(ReplacementTransform(holder, calculation[2]))

        # Transforms activations into calculation
        self.play(ReplacementTransform(a2.copy(), calculation[3][1]))

        # Writes calculation
        self.play(
            Write(calculation[0:2]), Write(calculation[3][0]), Write(calculation[3][2])
        )

        # Transforms result to weight error
        self.play(ReplacementTransform(calculation[0].copy(), w2e))

        # Uncreate equation, sans error
        self.play(Uncreate(calculation[0:2]), Uncreate(calculation[3]))
        self.wait()

        # Sets hidden neuron error
        # ----------------------------------------------------------

        # Sets equation hightlight
        wEqSelected = retainTransform(self, wEqSelected, errorEqSelected)

        z1e.scale(equation_scale)

        w2_scaled = w2.copy()
        w2_scaled.scale(1 / store_scale)
        w2_scaled.scale(equation_scale)

        z1_scaled = z1.copy()
        z1_scaled.scale(1 / store_scale)
        z1_scaled.scale(equation_scale)

        holder = calculation[2]  # delta_l-1

        # Sets calculation
        calculation = VGroup(
            z1e.copy(),
            MathTex("="),
            VGroup(MathTex(r"("), w2_scaled, MathTex(r")^T")),
            z2e.copy(),
            MathTex(r"\odot"),
            VGroup(MathTex(r"\sigma ' ("), z1_scaled.copy(), MathTex(r")")),
        )
        calculation[2].arrange(buff=equation_buffer)
        calculation[5].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calcualtion to side equations
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        # Shifts highlight box to match matricies shift

        n1Selected.shift(8 * RIGHT)

        values_sans_input_errors = VGroup(
            a1, w1, w1e[1:3], z1, b1, b1e[1:3], a2, w2, w2e, z2, b2, b2e, a3
        )

        w1e[0].shift(8 * RIGHT)
        b1e[0].shift(8 * RIGHT)

        shifted_values_sans_input_errors = values_sans_input_errors.copy()
        shifted_values_sans_input_errors.shift(8 * RIGHT)

        mid_xor_net[0][2][0][0].set_color(WHITE)
        mid_xor_net[0][2][1][0].set_color(WHITE)
        mid_xor_net[1][1].set_color(WHITE)
        # Highlights output
        mid_xor_net[0][1].set_color(YELLOW)
        mid_xor_net[1][0].set_color(YELLOW)
        self.play(
            ReplacementTransform(n2Selected, n1Selected),
            ReplacementTransform(
                values_sans_input_errors, shifted_values_sans_input_errors
            ),  # Shifts so it is visible
            Write(mid_xor_net[0][1]),
            Write(mid_xor_net[1][0]),
        )

        # Shifts matricies highlight box
        self.play(ReplacementTransform(n2Selected, n1Selected))

        # Pulls transforms matricies into calculation
        self.play(ReplacementTransform(holder, calculation[3]))
        self.play(ReplacementTransform(z1.copy(), calculation[5][1]))
        self.play(ReplacementTransform(w2.copy(), calculation[2][1]))

        # Write calculation, avoiding re-writing transformed in matricies
        self.play(
            Write(calculation[0:2]),
            Write(calculation[2][0]),
            Write(calculation[2][2]),
            Write(calculation[4]),
            Write(calculation[5][0]),
            Write(calculation[5][2]),
        )
        self.wait(10)  # After this, everything is repeated

        # Uncreate calculation, sans error
        self.play(Uncreate(calculation[1:6]))
        self.wait()

        # Sets hidden bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        errorEqSelected = retainTransform(self, errorEqSelected, bEqSelected)

        holder = calculation[0]

        b1e_scaled = b1e.copy()
        b1e_scaled.scale(1 / store_scale)
        b1e_scaled.scale(equation_scale)

        calculation = VGroup(b1e_scaled, MathTex("="), z1e.copy(), bu.copy())
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        self.play(ReplacementTransform(holder, calculation[2]))

        # Writes calculation
        self.play(Write(calculation[0:2]), Write(calculation[3]))

        # Transforms result to bias error
        self.play(ReplacementTransform(calculation[0].copy(), b1e))

        # Uncreate calculation, sans error
        self.play(Uncreate(calculation[0:2]), Uncreate(calculation[3]))

        # Sets hidden weight error
        # ----------------------------------------------------------

        # Sets equation hightlight
        bEqSelected = retainTransform(self, bEqSelected, wEqSelected)

        w1e_scaled = w1e.copy()
        w1e_scaled.scale(1 / store_scale)
        w1e_scaled.scale(equation_scale)

        a1_scaled = a1.copy()
        a1_scaled.scale(1 / store_scale)
        a1_scaled.scale(equation_scale)

        holder = calculation[2]
        calculation = VGroup(
            w1e_scaled,
            MathTex("="),
            z1e.copy(),
            VGroup(MathTex(r"("), a1_scaled, MathTex(r")^T")),
        )
        calculation[3].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        self.play(ReplacementTransform(holder, calculation[2]))

        # Transform matrix into calculation
        self.play(ReplacementTransform(a1.copy(), calculation[3][1]))

        # Writes calculation
        self.play(
            Write(calculation[0:2]), Write(calculation[3][0]), Write(calculation[3][2])
        )

        # Transforms result to weight error
        self.play(ReplacementTransform(calculation[0].copy(), w1e))

        # Uncreates calculation
        self.play(Uncreate(calculation))

        self.wait(1)  # Big pause before big explanation and end

        minus = MathTex("-")
        minus.scale(0.5)

        calculation = VGroup(
            VGroup(w1.copy(), minus.copy(), w1e.copy()),
            VGroup(b1.copy(), minus.copy(), b1e.copy()),
            VGroup(w2.copy(), minus.copy(), w2e.copy()),
            VGroup(b2.copy(), minus.copy(), b2e.copy()),
        )

        calculation[0].arrange(buff=0.1)
        calculation[1].arrange(buff=0.1)
        calculation[2].arrange(buff=0.1)
        calculation[3].arrange(buff=0.1)

        calculation.arrange(buff=0.4)

        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                calculation.get_y(),
                calculation.get_z(),
            ]
        )

        self.play(
            Write(calculation[0][1]),
            Write(calculation[1][1]),
            Write(calculation[2][1]),
            Write(calculation[3][1]),
        )

        self.play(
            ReplacementTransform(w1.copy(), calculation[0][0]),
            ReplacementTransform(w1e.copy(), calculation[0][2]),
            ReplacementTransform(b1.copy(), calculation[1][0]),
            ReplacementTransform(b1e.copy(), calculation[1][2]),
            ReplacementTransform(w2.copy(), calculation[2][0]),
            ReplacementTransform(w2e.copy(), calculation[2][2]),
            ReplacementTransform(b2.copy(), calculation[3][0]),
            ReplacementTransform(b2e.copy(), calculation[3][2]),
        )

    def construct(self):

        # Scene 1: Title screen
        # -----------------------------
        self.play_intro()

        # Scene 2: Equations
        # -----------------------------
        title, side_equations = self.play_equations()

        # Scene 3: Backprop
        # -----------------------------
        self.play_batch_backpropagation(title, side_equations)
