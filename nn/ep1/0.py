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

# Foreprop
class ep1_0(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.0, "Forepropagation")

        self.add(title_scene)

        self.wait(SCENE_WAIT)

        self.play(Uncreate(title_scene))

    def play_note_on_3b3b1(self):
        text = Text(
            "First check out 3Blue1Browns neural network series before watching this."
        )
        text.scale(0.5)
        img = ImageMobject("../../3b1b nets.png")
        # img.scale(1)

        text.next_to(img, UP)

        self.play(Write(text), FadeIn(img))

        self.wait(SCENE_WAIT)

        self.play(Unwrite(text), FadeOut(img))

    def play_mnist_net(self, scale=0.5):
        UP = [
            Circle(radius=0.15, stroke_color=WHITE, stroke_width=1)
            for i in range(0, 10)
        ]
        bottom = [
            Circle(radius=0.15, stroke_color=WHITE, stroke_width=1)
            for i in range(0, 10)
        ]
        inputs = VGroup(*UP, MathTex("\\vdots"), *bottom)
        inputs.arrange(DOWN)
        inputs = VGroup(Text("784"), Brace(inputs, LEFT), inputs)
        inputs.arrange()

        hidden1 = VGroup(
            *[
                Circle(radius=0.15, stroke_color=WHITE, stroke_width=1)
                for i in range(0, 16)
            ]
        )
        hidden1.arrange(DOWN)
        hidden2 = hidden1.copy()

        outputs = VGroup(
            *[
                VGroup(
                    Circle(radius=0.15, stroke_color=WHITE, stroke_width=1),
                    Text(str(i)),
                )
                for i in range(0, 10)
            ]
        )
        for group in outputs:
            group.arrange()

        outputs.arrange(DOWN)

        neurons = VGroup(inputs, hidden1, hidden2, outputs)
        neurons.arrange(buff=2)

        UP_edges = VGroup(
            *[
                Line(n1.get_center(), n2.get_center(), stroke_width=0.2)
                for n1 in UP
                for n2 in hidden1
            ]
        )
        bottom_edges = VGroup(
            *[
                Line(n1.get_center(), n2.get_center(), stroke_width=0.2)
                for n1 in bottom
                for n2 in hidden1
            ]
        )

        hidden_edges = VGroup(
            *[
                Line(n1.get_center(), n2.get_center(), stroke_width=0.2)
                for n1 in hidden1
                for n2 in hidden2
            ]
        )

        output_edges = VGroup(
            *[
                Line(n1.get_center(), n2[0].get_center(), stroke_width=0.2)
                for n1 in hidden2
                for n2 in outputs
            ]
        )

        connections = VGroup(UP_edges, bottom_edges, hidden_edges, output_edges)
        # net.scale(0.4)

        mnist_net = VGroup(neurons, connections)
        mnist_net.scale(scale)

        mnist_text = Text("MNIST")
        scene = VGroup(mnist_text, mnist_net)
        scene.arrange(DOWN)

        self.play(Write(mnist_text))
        self.play(Write(neurons))
        self.play(Write(connections))

        return (mnist_net, mnist_text)

    def play_xor_net(
        self, mnist_net, mnist_text, scale=0.8, shift=3.5, arrow_spacing=0.05
    ):
        xor_net = get_xor_net(1, 0.75, 2)
        xor_net.move_to(mnist_net.get_center())
        xor_net.scale(scale)

        xor_text = Text("XOR")
        xor_text.move_to(mnist_text.get_center())

        xor = VGroup(xor_text, xor_net)
        xor.shift(shift * RIGHT)

        self.play(
            Transform(mnist_net, mnist_net.copy().shift(shift * LEFT)),
            Transform(mnist_text, mnist_text.copy().shift(shift * LEFT)),
        )

        arrow = Arrow(
            ORIGIN + shift * LEFT + [arrow_spacing + mnist_net.get_width() / 2, 0, 0],
            ORIGIN + shift * RIGHT - [arrow_spacing + xor_net.get_width() / 2, 0, 0],
        )
        self.play(Write(arrow))
        self.play(Write(xor_text))
        self.play(Write(xor_net))

        self.wait(SCENE_WAIT)

        self.play(Uncreate(mnist_net), Uncreate(mnist_text), Uncreate(arrow))

        return (xor_net, xor_text)

    def play_xor_dataset(self, xor_net, xor_text):
        inputs = VGroup(
            Matrix([[0, 0]], h_buff=0.5),
            Matrix([[1, 0]], h_buff=0.5),
            Matrix([[0, 1]], h_buff=0.5),
            Matrix([[1, 1]], h_buff=0.5),
        )
        inputs.arrange(DOWN)
        inputs = VGroup(Text("Inputs"), inputs)
        inputs.arrange(DOWN)

        false = VGroup(Matrix([[1, 0]], h_buff=0.5), Text("False"))
        true = VGroup(Matrix([[0, 1]], h_buff=0.5), Text("True"))

        outputs = VGroup(false.copy(), true.copy(), true.copy(), false.copy())
        for output in outputs:
            output.arrange()
        outputs.arrange(DOWN)
        outputs = VGroup(Text("Outputs"), outputs)
        outputs.arrange(DOWN)

        labels = Matrix(matrix=[[0, 1, 1, 0]], v_buff=1.15)
        labels = VGroup(Text("Labels"), labels)
        labels.arrange(DOWN)

        moved_xor = xor_net.copy()

        scene = VGroup(inputs, outputs, labels, moved_xor)
        scene.arrange(buff=2.5)
        scene.scale(0.5)

        self.play(
            Transform(
                xor_text, xor_text.copy().move_to(ORIGIN + [0, xor_text.get_y(), 0])
            )
        )

        self.play(Transform(xor_net, moved_xor))

        self.play(Write(inputs))

        self.play(Write(outputs))

        self.play(Write(labels))

        self.wait(SCENE_WAIT)

        self.play(Uncreate(scene[0:3]), Uncreate(xor_text))

    def play_xor_values(self, xor_net):
        # Sets up wide XOR net
        # -----------------------------
        wide_xor_net = get_xor_net(0.5, 0.25, 4)

        # Define some useful aliases
        # -----------------------------
        inputs = wide_xor_net[0][0]
        hidden = wide_xor_net[0][1]
        outputs = wide_xor_net[0][2]

        input_edges = wide_xor_net[1][0]
        output_edges = wide_xor_net[1][1]

        # Sets up vague value matricies
        # -----------------------------
        z1 = MathTex(
            r"""
        \begin{bmatrix}
            z_{1,1} \\[6pt] z_{1,2} \\[6pt] z_{1,3}
        \end{bmatrix}
        """
        )
        z2 = MathTex(
            r"""
        \begin{bmatrix}
            z_{2,1} \\[6pt] z_{2,2}
        \end{bmatrix}
        """
        )

        a1 = MathTex(
            r"""
        \begin{bmatrix}
            a_{1,1} \\[6pt] a_{1,2}
        \end{bmatrix}
        """
        )
        a2 = MathTex(
            r"""
        \begin{bmatrix}
            a_{2,1} \\[6pt] a_{2,2} \\[6pt] a_{2,3}
        \end{bmatrix}
        """
        )
        a3 = MathTex(
            r"""
        \begin{bmatrix}
            a_{3,1} \\[6pt] a_{3,2}
        \end{bmatrix}
        """
        )

        w1 = MathTex(
            r"""
        \begin{bmatrix}
            w_{1,1,1} & w_{1,1,2} \\[6pt]
            w_{1,2,1} & w_{1,2,2} \\[6pt]
            w_{1,3,1} & w_{1,3,2}
        \end{bmatrix}
        """,
            color=RED,
        )
        w2 = MathTex(
            r"""
        \begin{bmatrix}
            w_{2,1,1} & w_{2,1,2} & w_{2,1,3} \\[6pt]
            w_{2,2,1} & w_{2,2,2} & w_{2,2,3}
        \end{bmatrix}
        """,
            color=RED,
        )

        b1 = MathTex(
            r"""
        \begin{bmatrix}
            b_{1,1} \\[6pt] b_{1,2} \\[6pt] b_{1,3}
        \end{bmatrix}
        """,
            color=BLUE,
        )
        b2 = MathTex(
            r"""
        \begin{bmatrix}
            b_{2,1} \\[6pt] b_{2,2}
        \end{bmatrix}
        """,
            color=BLUE,
        )

        # Sets groups for hidden and output layer neurons
        # -----------------------------
        n1 = VGroup(b1, z1, a2)
        n1.arrange()
        n2 = VGroup(b2, z2, a3)
        n2.arrange()

        # Scale and align all matrices
        # -----------------------------
        values = VGroup(a1, w1, n1, w2, n2)
        values.scale(0.4)
        values.arrange()

        # Sets scene arrangement
        # -----------------------------
        title = Text("What values are we looking at?")
        scene = VGroup(title, values, wide_xor_net)
        scene.arrange(DOWN, buff=1)

        # Horizontally aligns matrices over respective network sections
        # -----------------------------
        # Doing horizontal alignment manually since can't figure out `align_to`
        a1.move_to([inputs.get_x(), a1.get_y(), a1.get_z()])
        n1.move_to([hidden.get_x(), n1.get_y(), n1.get_z()])
        n2.move_to([outputs[0][0].get_x(), n2.get_y(), n2.get_z()])

        w1.move_to([input_edges.get_x(), w1.get_y(), w1.get_z()])
        w2.move_to([output_edges.get_x(), w2.get_y(), w2.get_z()])

        # Transforms from old xor net to new xor net (which is lower and wider)
        # -----------------------------
        self.play(ReplacementTransform(xor_net, wide_xor_net))

        # Writes title
        # -----------------------------
        self.play(Write(scene[0]))

        self.play(ReplacementTransform(inputs.copy(), a1))

        outputGroup = VGroup(outputs[0][0], outputs[1][0])
        # Illutrates b's, z's and a's
        self.play(
            ReplacementTransform(hidden.copy(), n1),
            ReplacementTransform(outputGroup.copy(), n2),
        )
        # Illutrates w's
        self.play(
            ReplacementTransform(input_edges.copy(), w1),
            ReplacementTransform(output_edges.copy(), w2),
        )

        self.wait(SCENE_WAIT)

        self.play(Uncreate(title))

        return (values, wide_xor_net)

    def play_equations(self, values, wide_xor_net):
        # Gets small XOR net
        mid_xor_net = get_xor_net(0.5, 0.25, 2)

        # Shifts matrices up
        moved_values = values.copy()
        moved_values.shift(1.5 * UP)

        # Shifts net down
        mid_xor_net.move_to(wide_xor_net.get_center())
        mid_xor_net.shift(1 * DOWN)

        # Transforms to new matrices and new net
        self.play(
            ReplacementTransform(wide_xor_net, mid_xor_net),
            ReplacementTransform(values, moved_values),
        )

        side_equations = get_equations(
            equations=[r"a^{l+1} = A(z^l)", r"z^l = w^l a^l + b^l"]
        )

        title = Text("Foreprop Equations")
        title.move_to(side_equations.get_center() + 3 * UP)

        self.play(Write(title))

        self.play(Write(side_equations))

        self.wait(SCENE_WAIT)

        self.play(
            ReplacementTransform(side_equations, side_equations.copy().shift(5 * LEFT))
        )

        self.play(Uncreate(title))

        return (side_equations, moved_values, mid_xor_net)

    def play_forepropagation(
        self, moved_values, net, side_equations, store_scale=0.5, equation_scale=0.7
    ):
        # Define some useful aliases
        # -----------------------------
        side_equations_alignment = (
            side_equations.get_x() + side_equations.get_width() / 2 + 0.5
        )

        wide_xor_net = net

        inputs = wide_xor_net[0][0]
        hidden = wide_xor_net[0][1]
        outputs = wide_xor_net[0][2]
        input_edges = wide_xor_net[1][0]
        output_edges = wide_xor_net[1][1]

        # Sets up matricies with values
        a1 = Matrix([["0"], ["1"]], h_buff=1.2)
        a2 = Matrix([["0.47..."], ["0.62..."], ["0.52..."]], h_buff=1.2)
        a3 = Matrix([["0.62..."], ["0.53..."]], h_buff=1.2)

        z1 = Matrix([["-0.1"], ["0.5"], ["0.1"]], h_buff=1.2)
        z2 = Matrix([["0.49..."], ["0.12..."]], h_buff=1.5)

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
        w2 = MathTex(
            r"""
        \begin{bmatrix}
            -0.2 & 0.2 & 0.5 \\[6pt]
            0.1 & 0.2 & 0.3
        \end{bmatrix}
        """,
            color=RED,
        )

        b1 = MathTex(
            r"""
        \begin{bmatrix}
            -0.3 \\[6pt] 0.3 \\[6pt] 0.6
        \end{bmatrix}
        """,
            color=BLUE,
        )
        b2 = MathTex(
            r"""
        \begin{bmatrix}
            0.2 \\[6pt] -0.2
        \end{bmatrix}
        """,
            color=BLUE,
        )

        # Sets up matricies
        net_values_precise = VGroup(a1, w1, b1, z1, a2, w2, b2, z2, a3)
        net_values_precise.scale(store_scale)  # Scales up matrices
        net_values_precise.arrange()
        net_values_precise.move_to(moved_values.get_center())

        # ------------------------------------------------------------------------------------
        # Sets up highlights boxes
        # ------------------------------------------------------------------------------------

        eqZ = get_highlight_box(side_equations[0][1])
        eqA = get_highlight_box(side_equations[0][0])

        foreprop_header = Text("Foreprogation")
        foreprop_header.shift(3 * UP)

        # Transforms to precise values (leaving out a and z values)
        # Done by each matrix to make it clearer
        self.play(
            Write(foreprop_header),
            ReplacementTransform(moved_values[0], a1[1:3]),
            ReplacementTransform(moved_values[1], w1),
            ReplacementTransform(moved_values[2][0], z1[1:3]),
            ReplacementTransform(moved_values[2][1], b1),
            ReplacementTransform(moved_values[2][2], a2[1:3]),
            ReplacementTransform(moved_values[3], w2),
            ReplacementTransform(moved_values[4][0], z2[1:3]),
            ReplacementTransform(moved_values[4][1], b2),
            ReplacementTransform(moved_values[4][2], a3[1:3]),
        )

        self.wait(SCENE_WAIT)

        # ------------------------------------------------------------------------------------
        # a1
        # ------------------------------------------------------------------------------------

        # Highlights input neurons
        inputs.set_color(YELLOW)
        self.play(Write(inputs))

        # Highlights matricies
        a1_highlight = get_highlight_box(VGroup(a1))
        self.play(Write(a1_highlight))

        # Sets a1
        a1_scaled = rescale(a1.copy(), store_scale, equation_scale)
        a1_a1_scaled = (
            a1_scaled.copy()
        )  # Re-used later, so we don't use and uncreate the base version

        a1_a1_scaled.center()

        # Writes a1
        self.play(Write(a1_a1_scaled))
        # Stores a1
        self.play(ReplacementTransform(a1_a1_scaled.copy(), a1))

        self.wait(SCENE_WAIT)

        # Uncreates a1
        self.play(Uncreate(a1_a1_scaled))

        # ------------------------------------------------------------------------------------
        # z1
        # ------------------------------------------------------------------------------------

        # Highlights equation
        self.play(Write(eqZ))

        # Highlights matricies
        z1_highlight = get_highlight_box(VGroup(a1, w1, b1, z1))
        self.play(ReplacementTransform(a1_highlight, z1_highlight))

        # Highlights input edges
        inputs.set_color(WHITE)
        input_edges.set_color(YELLOW)
        hidden.set_color(YELLOW)
        self.play(
            Write(input_edges), Write(hidden)  # Re-writes edges  # Re-writes to update
        )

        z1_scaled = rescale(z1.copy(), store_scale, equation_scale)
        z1_z1_scaled = (
            z1_scaled.copy()
        )  # Re-used later, so we don't use and uncreate the base version

        w1_scaled = rescale(w1.copy(), store_scale, equation_scale)

        b1_scaled = rescale(b1.copy(), store_scale, equation_scale)

        z1_a1_scaled = a1_scaled.copy()

        # Sets z1 calculation
        z1_calculation = VGroup(
            z1_z1_scaled, MathTex("="), z1_a1_scaled, w1_scaled, MathTex("+"), b1_scaled
        )
        z1_calculation.arrange()

        # Pulls a1 into equation
        self.play(ReplacementTransform(a1.copy(), z1_a1_scaled))
        # Pulls w1 into equation
        self.play(ReplacementTransform(w1.copy(), w1_scaled))
        # Pulls b1 into equation
        self.play(ReplacementTransform(b1.copy(), b1_scaled))

        # Writes operations
        self.play(
            Write(z1_z1_scaled), Write(z1_calculation[1]), Write(z1_calculation[4])
        )

        # Stores z1
        self.play(ReplacementTransform(z1_z1_scaled.copy(), z1))

        self.wait(SCENE_WAIT)

        # Clears z1 calculation
        self.play(Uncreate(z1_calculation))

        # ------------------------------------------------------------------------------------
        # a2
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqZ = retainTransform(self, eqZ, eqA)

        # Highlights matricies
        a2_highlight = get_highlight_box(VGroup(z1, a2))
        self.play(ReplacementTransform(z1_highlight, a2_highlight))

        a2_scaled = rescale(a2.copy(), store_scale, equation_scale)
        a2_a2_scaled = (
            a2_scaled.copy()
        )  # Re-used later, so we don't use and uncreate the base version

        a2_z1_scaled = z1_scaled.copy()

        a2_calculation = VGroup(
            a2_a2_scaled,
            MathTex("="),
            MathTex(r"\sigma \Big("),
            a2_z1_scaled,
            MathTex(r"\Big)"),
        )
        a2_calculation.arrange()

        # Pulls z1 into equation
        self.play(ReplacementTransform(z1.copy(), a2_z1_scaled))

        # Writes operations
        self.play(
            Write(a2_a2_scaled), Write(a2_calculation[1:3]), Write(a2_calculation[4])
        )

        # Stores a2
        self.play(ReplacementTransform(a2_a2_scaled.copy(), a2))

        self.wait(SCENE_WAIT)

        # Clears equation
        self.play(Uncreate(a2_calculation))

        # ------------------------------------------------------------------------------------
        # z2
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqA = retainTransform(self, eqA, eqZ)

        # Highlights matricies
        z2_highlight = get_highlight_box(VGroup(a2, w2, b2, z2))
        self.play(ReplacementTransform(a2_highlight, z2_highlight))

        # Highlights 1st hidden layer
        input_edges.set_color(WHITE)
        hidden.set_color(WHITE)
        output_edges.set_color(YELLOW)
        outputs.set_color(YELLOW)
        self.play(
            # Re-writes to update
            Write(input_edges),
            Write(hidden),
            Write(output_edges),
            Write(outputs),
        )

        w2_scaled = rescale(w2.copy(), store_scale, equation_scale)

        z2_a2_scaled = a2_scaled.copy()

        b2_scaled = rescale(b2.copy(), store_scale, equation_scale)
        # Could scale this to match size of `input_weight_result`, but honestly who cares, this just adds unneccessary complexitity

        z2_scaled = rescale(z2.copy(), store_scale, equation_scale)
        z2_z2_scaled = (
            z2_scaled.copy()
        )  # Re-used later, so we don't use and uncreate the base version

        z2_calculation = VGroup(
            z2_z2_scaled, MathTex("="), w2_scaled, z2_a2_scaled, MathTex("+"), b2_scaled
        )
        z2_calculation.arrange()

        # Aligns to side equations.
        #  Only needed here bc this is the only equation in this video
        #  which doesn't fit otherwise.
        z2_calculation.move_to(
            [
                side_equations_alignment + z2_calculation.get_width() / 2,
                z2_calculation.get_y(),
                z2_calculation.get_z(),
            ]
        )

        # Pulls input weights into equation
        self.play(ReplacementTransform(a2.copy(), z2_a2_scaled))
        # Pulls input weights into equation
        self.play(ReplacementTransform(w2.copy(), w2_scaled))
        # Pulls biases into equation
        self.play(ReplacementTransform(b2.copy(), b2_scaled))
        # Writes operations
        self.play(
            Write(z2_z2_scaled), Write(z2_calculation[1]), Write(z2_calculation[4])
        )
        # Store result into matricies
        self.play(ReplacementTransform(z2_z2_scaled.copy(), z2))
        # Clears equation
        self.play(Uncreate(z2_calculation))

        # ------------------------------------------------------------------------------------
        # a3
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqZ = retainTransform(self, eqZ, eqA)

        a3_highlight = get_highlight_box(VGroup(z2, a3))
        self.play(ReplacementTransform(z2_highlight, a3_highlight))

        a3_scaled = rescale(a3.copy(), store_scale, equation_scale)

        a3_z2_scaled = z2_scaled.copy()

        a3_calculation = VGroup(
            a3_scaled,
            MathTex("="),
            MathTex(r"\sigma \Big("),
            a3_z2_scaled,
            MathTex(r"\Big)"),
        )
        a3_calculation.arrange()

        # Pulls z2 into calculation
        self.play(ReplacementTransform(z2.copy(), a3_z2_scaled))

        self.play(
            Write(a3_scaled),
            Write(a3_calculation[1:3]),
            Write(a3_calculation[4]),
        )

        # Stores a3
        self.play(ReplacementTransform(a3_scaled.copy(), a3))

        self.play(Uncreate(a3_calculation))

        # Done
        # ------------------------------------------------------------------------------------

        self.play(Write(Text("Done.")))

        self.wait(SCENE_WAIT)

    def construct(self):
        # Scene 1: Title screen
        # -----------------------------
        self.play_intro()

        # Scene 2: See 3b1b's video first
        # -----------------------------
        self.play_note_on_3b3b1()

        # Scene 3: MNIST net
        # -----------------------------
        mnist_net, mnist_text = self.play_mnist_net()

        # Scene 4: XOR net
        # -----------------------------
        xor_net, xor_text = self.play_xor_net(mnist_net, mnist_text)

        # Scene 5: Dataset
        # -----------------------------
        self.play_xor_dataset(xor_net, xor_text)

        # Scene 6: Values in net
        # -----------------------------
        values, net = self.play_xor_values(xor_net)

        # Scene 7: Foreprop equations
        # -----------------------------
        equations, values, net = self.play_equations(values, net)

        # Scene 8: Does foreprop
        # -----------------------------
        self.play_forepropagation(values, net, equations)
