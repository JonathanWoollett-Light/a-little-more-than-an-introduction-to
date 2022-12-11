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

# Backprop
class ep1_1(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.1, "Backpropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_equations(self):
        side_equations = get_equations(
            equations=[
                r"\delta^L = \nabla_a C \odot A'(z^L)",
                r"\delta^l = (w^{l+1})^T \delta^{l+1} \odot A'(z^l)",
                r"\frac{\partial C}{\partial b^l} = \delta^l",
                r"\frac{\partial C}{\partial w^l} = \delta^l (a^l)^T",
            ],
            wheres=[r"\delta^l = \frac{\partial C}{\partial z^l}"],
            scale=0.3,
        )

        title = Text("Backpropagation")
        title.move_to(side_equations.get_center() + 3 * UP)

        self.play(Write(title))
        self.wait(3)
        self.play(Write(side_equations))
        self.wait(3)

        self.play(
            ReplacementTransform(side_equations, side_equations.copy().shift(5 * LEFT))
        )

        return (title, side_equations)

    def play_backpropagation(self, title, side_equations, store_scale=0.3):

        # Sets up matricies with values
        # ----------------------------------------------------------
        a1 = Matrix([["0"], ["1"]], h_buff=1.2)
        a2 = Matrix([["0.47..."], ["0.62..."], ["0.52..."]], h_buff=1.2)
        a3 = Matrix([["0.62..."], ["0.53..."]], h_buff=1.2)

        z1 = Matrix([["-0.1"], ["0.5"], ["0.1"]], h_buff=1.2)
        z2 = Matrix([["0.29..."], ["0.33..."]], h_buff=1.5)

        w1 = MathTex(
            r"""
        \begin{bmatrix}
            -0.2 & 0.2 \\[6pt]
            0.1 & 0.2 \\[6pt]
            0.5 & -0.5
        \end{bmatrix}
        """,
            color=RED,
        )
        w1e = Matrix(
            [["0", "-0.01..."], ["0", "0.00..."], ["0", "0.00..."]], h_buff=2
        ).set_color(GREEN)
        w2 = MathTex(
            r"""
        \begin{bmatrix}
            -0.2 & 0.2 & 0.5 \\[6pt]
            0.1 & 0.2 & 0.3
        \end{bmatrix}
        """,
            color=RED,
        )
        w2e = Matrix(
            [["0.06...", "0.09...", "0.07..."], ["-0.05...", "-0.07...", "-0.06..."]],
            h_buff=2,
        ).set_color(GREEN)

        b1 = MathTex(
            r"""
        \begin{bmatrix}
            -0.3 \\[6pt] 0.3 \\[6pt] 0.6
        \end{bmatrix}
        """,
            color=BLUE,
        )
        b1e = Matrix([["-0.01..."], ["0.00..."], ["0.00..."]]).set_color(GREEN)
        b2 = MathTex(
            r"""
        \begin{bmatrix}
            0.2 \\[6pt] -0.2
        \end{bmatrix}
        """,
            color=BLUE,
        )
        b2e = Matrix([["0.14..."], ["-0.11..."]]).set_color(GREEN)

        n1 = VGroup(w1e, b1, b1e, z1, a2)
        n2 = VGroup(w2e, b2, b2e, z2, a3)

        # Scales all matricies
        net_values_precise = VGroup(
            a1, w1, w1e, b1, b1e, z1, a2, w2, w2e, b2, b2e, z2, a3
        )
        net_values_precise.arrange()
        net_values_precise.scale(store_scale)  # Scales down matricies

        title_and_values = VGroup(title.copy(), net_values_precise)
        title_and_values.arrange(DOWN)

        # Sets net
        # -----------------------------
        mid_xor_net = get_xor_net(0.5, 0.25, 2)

        # Sets intial scene
        # ----------------------------------------------------------
        a3_scaled = a3.copy()
        a3_scaled.scale(1 / store_scale)

        equation = MathTex(r"\delta^L", "=", r"\nabla_a C", r"\odot", r"A'(z^L)")

        current = VGroup(a3_scaled, equation)
        current.arrange(DOWN)

        scene = VGroup(title_and_values, current, mid_xor_net)
        scene.arrange(DOWN, buff=1.25)

        mid_xor_net.shift(0.2 * UP)

        net_values_precise_excluding_errors = VGroup(
            a1, w1, w1e[1:3], z1, b1, b1e[1:3], a2, w2, w2e[1:3], z2, b2, b2e[1:3], a3
        )

        self.play(ReplacementTransform(title, title_and_values[0]))
        self.play(
            Write(net_values_precise_excluding_errors),
            Write(a3_scaled),
            Write(mid_xor_net),
        )
        self.wait(10)

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

        # Sets output neuron error
        # ----------------------------------------------------------

        # Sets equation hightlight
        self.play(Write(outErrorEqSelected))

        target = Matrix([["0"], ["1"]], h_buff=1)

        # Result
        output_cz_derivative = Matrix([["0.14..."], ["-0.11..."]], h_buff=1.75)

        # Sets calculation
        calculation = VGroup(
            output_cz_derivative.copy(),
            MathTex("="),
            VGroup(a3_scaled.copy(), MathTex("-"), target),
            MathTex(r"\odot"),
            VGroup(
                MathTex(r"\Bigg("),
                a3_scaled.copy(),
                MathTex(r"\odot"),
                MathTex(r"\bigg(1-"),
                a3_scaled.copy(),
                MathTex(r"\bigg)"),
                MathTex(r"\Bigg)"),
            ),
        )
        calculation.scale(0.4)
        calculation[2].arrange(buff=0.1)
        calculation[4].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        side_equations_alignment = (
            side_equations.get_x() + side_equations.get_width() / 2 + 0.5
        )
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
            ]
        )

        # Aligns equation to calculation
        align_horizontally(calculation, equation)

        # Highlights output
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
        self.play(ReplacementTransform(a3_scaled.copy(), calculation[4][1]))
        self.play(ReplacementTransform(calculation[4][1].copy(), calculation[4][4]))

        self.play(
            Write(calculation[1]),
            Write(calculation[2][1]),
            Write(calculation[2][2]),
            Write(calculation[3]),
            Write(calculation[4][0]),
            Write(calculation[4][2:4]),
            Write(calculation[4][5:7]),
        )

        self.play(ReplacementTransform(side_equations[0][0][1].copy(), equation))
        self.wait()
        self.play(Write(calculation[0]))
        self.wait()

        sigmoid_derivative = MathTex(
            r"\sigma '(z)", r"= \sigma (z) (1- \sigma (z))", "= a(1-a)"
        )
        sigmoid_derivative.scale(0.6)
        sigmoid_derivative[2].move_to(
            [
                sigmoid_derivative[1].get_x()
                - sigmoid_derivative[1].get_width() / 2
                + sigmoid_derivative[2].get_width() / 2,
                sigmoid_derivative.get_y() - 1.2 * sigmoid_derivative.get_height(),
                sigmoid_derivative.get_z(),
            ]
        )
        sigmoid_derivative.move_to(equation[4].get_center())

        equation4_holder = equation[4].copy()
        self.play(ReplacementTransform(equation[4], sigmoid_derivative))
        self.wait(3)
        self.play(ReplacementTransform(sigmoid_derivative, equation4_holder))
        self.wait(3)

        # Left bit
        output_az_derivative = Matrix([["0.62..."], ["-0.46..."]], h_buff=1.75)
        output_az_derivative.scale(0.4)
        output_az_derivative.move_to(calculation[2].get_center())
        self.play(ReplacementTransform(calculation[2], output_az_derivative))
        self.wait()

        # Right bit
        output_ca_derivative_halfway = Matrix([["-0.37..."], ["-0.46..."]], h_buff=1.75)
        output_ca_derivative_halfway.scale(0.4)
        output_ca_derivative_halfway.move_to(calculation[4][3:6].get_center())
        self.play(
            ReplacementTransform(calculation[4][3:6], output_ca_derivative_halfway)
        )
        self.wait()

        output_ca_derivative = Matrix([["0.23..."], ["0.24.."]], h_buff=1.75)
        output_ca_derivative.scale(0.4)
        output_ca_derivative.move_to(calculation[4].get_center())
        self.play(
            ReplacementTransform(
                VGroup(calculation[4], output_ca_derivative_halfway),
                output_ca_derivative,
            )
        )
        self.wait()

        self.play(
            Uncreate(calculation[1]),
            Uncreate(calculation[3]),
            Uncreate(output_az_derivative),
            Uncreate(output_ca_derivative),
            Uncreate(equation[0:4]),
            Uncreate(equation4_holder),
        )

        # Sets output bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        outErrorEqSelected = retainTransform(self, outErrorEqSelected, bEqSelected)

        holder = calculation[0]

        b2e_scaled = b2e.copy()
        b2e_scaled.scale(1 / store_scale)

        calculation = VGroup(b2e_scaled, MathTex("="), output_cz_derivative.copy())
        calculation.scale(0.4)
        calculation.arrange(buff=0.5)
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
            ]
        )

        self.play(ReplacementTransform(holder, calculation[2]))

        old_question_center = equation.get_center()
        equation = MathTex(r"\frac{\partial C}{\partial b^l}", "=", r"\delta^l")
        equation.move_to(old_question_center)

        # Horizontally aligns equation components to calculation components
        align_horizontally(calculation, equation)

        self.play(ReplacementTransform(side_equations[0][2][1].copy(), equation))
        self.wait()
        self.play(Write(calculation[0:2]))

        self.play(ReplacementTransform(calculation[0].copy(), b2e))

        self.play(Uncreate(calculation[0:2]), Uncreate(equation))

        # Sets output weight error
        # ----------------------------------------------------------

        # Sets equation hightlight
        bEqSelected = retainTransform(self, bEqSelected, wEqSelected)

        w2e_scaled = w2e.copy()
        w2e_scaled.scale(1 / store_scale)

        a2_scaled = a2.copy()
        a2_scaled.scale(1 / store_scale)

        holder = calculation[2]
        calculation = VGroup(
            w2e_scaled,
            MathTex("="),
            output_cz_derivative.copy(),
            VGroup(MathTex(r"\Bigg("), a2_scaled, MathTex(r"\Bigg)^T")),
        )
        calculation.scale(0.4)
        calculation[3].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
            ]
        )
        self.play(ReplacementTransform(holder, calculation[2]))

        old_question_center = equation.get_center()
        equation = MathTex(
            r"\frac{\partial C}{\partial w^l}", "=", r"\delta_l", r"(a^{l-1})^T"
        )
        equation.move_to(old_question_center)

        align_horizontally(calculation, equation)

        self.play(ReplacementTransform(side_equations[0][3][1].copy(), equation))

        self.play(ReplacementTransform(a2.copy(), calculation[3][1]))

        self.play(
            Write(calculation[0:2]), Write(calculation[3][0]), Write(calculation[3][2])
        )

        self.play(ReplacementTransform(calculation[0].copy(), w2e))

        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(calculation[3]),
            Uncreate(equation[0:2]),
            Uncreate(equation[3]),
        )

        self.wait(1)  # Explanation before repeat

        self.play(Uncreate(equation[2]))

        # Sets hidden neuron error
        # ----------------------------------------------------------

        # Sets equation hightlight
        wEqSelected = retainTransform(self, wEqSelected, errorEqSelected)

        old_question_center = equation.get_center()
        equation = MathTex(
            r"\delta^l", "=", r"(w^{l+1})^T", r"\delta^{l+1}", r"\odot", r"A'(z^l)"
        )
        equation.move_to(old_question_center)

        # Result
        hidden_cz_derivative = Matrix(
            [["-0.01..."], ["0.00..."], ["0.00..."]], h_buff=1.75
        )

        w2_scaled = w2.copy()
        w2_scaled.scale(1 / store_scale)

        a2_scaled = a2.copy()
        a2_scaled.scale(1 / store_scale)

        holder = calculation[2]  # delta_l-1

        # Sets calculation
        calculation = VGroup(
            hidden_cz_derivative.copy(),
            MathTex("="),
            VGroup(MathTex(r"\Bigg("), w2_scaled, MathTex(r"\Bigg)^T")),
            output_cz_derivative.copy(),
            MathTex(r"\odot"),
            VGroup(
                MathTex(r"\Bigg("),
                a2_scaled.copy(),
                MathTex(r"\odot"),
                MathTex(r"\bigg(1-"),
                a2_scaled.copy(),
                MathTex(r"\bigg)"),
                MathTex(r"\Bigg)"),
            ),
        )
        calculation.scale(0.4)
        calculation[2].arrange(buff=0.1)
        calculation[5].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
            ]
        )

        # Aligns equation to calculation
        align_horizontally(calculation, equation)

        mid_xor_net[0][2][0][0].set_color(WHITE)
        mid_xor_net[0][2][1][0].set_color(WHITE)
        mid_xor_net[1][1].set_color(WHITE)
        # Highlights output
        mid_xor_net[0][1].set_color(YELLOW)
        mid_xor_net[1][0].set_color(YELLOW)
        self.play(
            ReplacementTransform(n2Selected, n1Selected),
            Write(mid_xor_net[0][1]),
            Write(mid_xor_net[1][0]),
        )

        self.play(ReplacementTransform(n2Selected, n1Selected))

        self.play(ReplacementTransform(holder, calculation[3]))

        self.play(ReplacementTransform(side_equations[0][1][1].copy(), equation))

        self.play(ReplacementTransform(a2.copy(), calculation[5][1]))
        self.play(ReplacementTransform(calculation[5][1].copy(), calculation[5][4]))

        self.play(ReplacementTransform(w2.copy(), calculation[2][1]))

        self.play(
            Write(calculation[1]),
            Write(calculation[2][0]),
            Write(calculation[2][2]),
            Write(calculation[4]),
            Write(calculation[5][0]),
            Write(calculation[5][2:4]),
            Write(calculation[5][5:8]),
        )

        self.wait()
        self.play(Write(calculation[0]))

        self.wait(10)  # After this, everything is repeated

        self.play(Uncreate(calculation[1:6]))
        self.wait()
        self.play(Uncreate(equation))

        # Sets hidden bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        errorEqSelected = retainTransform(self, errorEqSelected, bEqSelected)

        holder = calculation[0]

        b1e_scaled = b1e.copy()
        b1e_scaled.scale(1 / store_scale)

        calculation = VGroup(b1e_scaled, MathTex("="), hidden_cz_derivative.copy())
        calculation.scale(0.4)
        calculation.arrange(buff=0.5)
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
            ]
        )

        self.play(ReplacementTransform(holder, calculation[2]))

        old_question_center = equation.get_center()
        equation = MathTex(r"\frac{\partial C}{\partial b^l}", "=", r"\delta^l")
        equation.move_to(old_question_center)

        # Horizontally aligns equation components to calculation components
        align_horizontally(calculation, equation)

        self.play(ReplacementTransform(side_equations[0][2][1].copy(), equation))
        self.wait()
        self.play(Write(calculation[0:2]))

        self.play(ReplacementTransform(calculation[0].copy(), b1e))

        self.play(Uncreate(calculation[0:2]), Uncreate(equation))

        # Sets hidden weight error
        # ----------------------------------------------------------

        # Sets equation hightlight
        bEqSelected = retainTransform(self, bEqSelected, wEqSelected)

        w1e_scaled = w1e.copy()
        w1e_scaled.scale(1 / store_scale)

        a1_scaled = a1.copy()
        a1_scaled.scale(1 / store_scale)

        holder = calculation[2]
        calculation = VGroup(
            w1e_scaled,
            MathTex("="),
            hidden_cz_derivative.copy(),
            VGroup(MathTex(r"\Bigg("), a1_scaled, MathTex(r"\Bigg)^T")),
        )
        calculation.scale(0.4)
        calculation[3].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
            ]
        )
        self.play(ReplacementTransform(holder, calculation[2]))

        old_question_center = equation.get_center()
        equation = MathTex(
            r"\frac{\partial C}{\partial w^l}", "=", r"\delta_l", r"(a^{l-1})^T"
        )
        equation.move_to(old_question_center)

        align_horizontally(calculation, equation)

        self.play(ReplacementTransform(side_equations[0][3][1].copy(), equation))

        self.play(ReplacementTransform(a1.copy(), calculation[3][1]))

        self.play(
            Write(calculation[0:2]), Write(calculation[3][0]), Write(calculation[3][2])
        )

        self.play(ReplacementTransform(calculation[0].copy(), w1e))

        self.play(Uncreate(calculation[0:4]), Uncreate(equation[0:4]))

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

        calculation.arrange(buff=0.5)

        calculation.move_to(
            [
                side_equations_alignment + calculation.get_width() / 2,
                current[0].get_y(),
                current[0].get_z(),
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

        self.wait(SCENE_WAIT)

    def construct(self):

        # Scene 1: Title screen
        # -----------------------------
        self.play_intro()

        # Scene 2: Equations
        # -----------------------------
        title, side_equations = self.play_equations()

        # Scene 3: Backprop
        # -----------------------------
        self.play_backpropagation(title, side_equations)
