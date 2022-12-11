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

# Batch foreprop
class ep1_2(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.2, "Batch forepropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_simd(self):
        v_buffer = 1.1

        simd_in = Matrix([[1], [2], [3], [4]], v_buff=v_buffer)
        simd_ones = Matrix([[1], [1], [1], [1]], v_buff=v_buffer)
        simd_out_pre = Matrix([["1+1"], ["2+1"], ["3+1"], ["4+1"]], v_buff=v_buffer)
        simd_out_post = Matrix([[2], [3], [4], [5]], v_buff=v_buffer)
        simd = VGroup(simd_in, MathTex("+"), simd_ones, MathTex("="), simd_out_pre)
        simd.arrange()

        sisd_out_pre = VGroup(
            Matrix([["1+1"]]), Matrix([["2+1"]]), Matrix([["3+1"]]), Matrix([["4+1"]])
        )
        sisd_out_post = VGroup(
            Matrix([[2]]), Matrix([[3]]), Matrix([[4]]), Matrix([[5]])
        )
        sisd = VGroup(
            VGroup(Matrix([[1]]), MathTex("+1="), sisd_out_pre[0]),
            VGroup(Matrix([[2]]), MathTex("+1="), sisd_out_pre[1]),
            VGroup(Matrix([[3]]), MathTex("+1="), sisd_out_pre[2]),
            VGroup(Matrix([[4]]), MathTex("+1="), sisd_out_pre[3]),
        )
        for row in sisd:
            row.arrange()
        sisd.arrange(DOWN)

        simd_title = Text("SIMD")
        simd_title.scale(1.5)
        sisd_title = Text("SISD")
        sisd_title.scale(1.5)

        scene = VGroup(VGroup(simd_title, simd), VGroup(sisd_title, sisd))
        title_distance = 1.2
        scene[0].arrange(DOWN, buff=title_distance)
        scene[1].arrange(DOWN, buff=title_distance)
        scene.arrange(buff=2)

        everything = VGroup(scene, simd_out_post, sisd_out_post)
        everything.scale(0.7)

        # Movement of unarranged things

        simd_out_post.move_to(simd_out_pre.get_center())
        for (post, pre) in zip(sisd_out_post, sisd_out_pre):
            post.move_to(pre.get_center())

        self.play(Write(scene))

        simd_box = Rectangle(
            color=YELLOW, height=simd.get_height() + 0.3, width=simd.get_width() + 0.3
        )
        sisd_box = Rectangle(
            color=YELLOW, height=sisd.get_height() + 0.3, width=sisd.get_width() + 0.3
        )
        # Moves highlight boxes to center on said thing they are highlighting
        simd_box.move_to(simd.get_center())
        sisd_box.move_to(sisd.get_center())

        self.play(Write(simd_box))

        self.play(ReplacementTransform(simd_out_pre[0], simd_out_post[0]))

        self.wait(2)

        self.play(ReplacementTransform(simd_box, sisd_box))

        self.play(ReplacementTransform(sisd_out_pre[0][0], sisd_out_post[0][0]))
        self.play(ReplacementTransform(sisd_out_pre[1][0], sisd_out_post[1][0]))
        self.play(ReplacementTransform(sisd_out_pre[2][0], sisd_out_post[2][0]))
        self.play(ReplacementTransform(sisd_out_pre[3][0], sisd_out_post[3][0]))

        self.wait(5)

        self.play(
            # Uncreate easy parts of equations
            Uncreate(simd[0:-1]),
            Uncreate(sisd[0][0:2]),
            Uncreate(sisd[1][0:2]),
            Uncreate(sisd[2][0:2]),
            Uncreate(sisd[3][0:2]),
            # Uncreate brackets
            Uncreate(simd_out_pre[1:3]),
            Uncreate(sisd_out_pre[0][1:3]),
            Uncreate(sisd_out_pre[1][1:3]),
            Uncreate(sisd_out_pre[2][1:3]),
            Uncreate(sisd_out_pre[3][1:3]),
            # Uncreates values
            Uncreate(simd_out_post[0]),
            Uncreate(sisd_out_post[0][0]),
            Uncreate(sisd_out_post[1][0]),
            Uncreate(sisd_out_post[2][0]),
            Uncreate(sisd_out_post[3][0]),
            # Uncreates titles
            Uncreate(simd_title),
            Uncreate(sisd_title),
            Uncreate(sisd_box),  # Uncreate highlight box
        )

        self.wait()

    def play_equations(self):
        side_equations = get_equations(
            equations=[r"a^{l+1} = A(z^l)", r"z^l = w^l a^l + b^l J_n"],
            wheres=[r"J_n=[1_1,...,1_n]"],
            scale=0.4,
        )

        title = Text("Foreprop Equations")
        title.move_to(side_equations.get_center() + 3 * UP)

        self.play(Write(title))
        self.play(Write(side_equations))

        self.wait()

        self.play(Uncreate(title))

        return side_equations

    def play_batch_forwardpropagation(
        self, side_equations, store_scale=0.3, equation_scale=0.4
    ):
        # Define some useful aliases
        # -----------------------------
        self.play(
            ReplacementTransform(side_equations, side_equations.copy().shift(5 * LEFT))
        )
        side_equations_alignment = (
            side_equations.get_x() + side_equations.get_width() / 2 + 0.5
        )

        # Sets up matricies with values
        a1 = Matrix([["0", "0", "1", "1"], ["0", "1", "0", "1"]])
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
        z2 = Matrix(
            [
                ["0.55...", "0.49...", "0.61...", "0.56..."],
                ["0.15...", "0.12...", "0.18...", "0.16..."],
            ],
            h_buff=1.5,
        )

        w1 = Matrix([[-0.2, 0.2], [0.1, 0.2], [0.5, -0.5]]).set_color(RED)
        w2 = Matrix([[-0.2, 0.2, 0.5], [0.1, 0.2, 0.3]]).set_color(RED)

        b1 = Matrix([[-0.3], [0.3], [0.6]]).set_color(BLUE)
        b2 = Matrix([[0.2], [-0.2]]).set_color(BLUE)
        bu = Matrix([[1, 1, 1, 1]], h_buff=0.7)

        # Sets up matricies
        net_values_precise = VGroup(a1, w1, b1, z1, a2, w2, b2, z2, a3)
        net_values_precise.arrange()
        net_values_precise.scale(store_scale)  # Scales up matricies
        # Shifts matricies up
        net_values_precise.shift(2 * UP)

        # Gets small XOR net
        mid_xor_net = get_xor_net(0.5, 0.25, 2)
        # Shifts net down
        mid_xor_net.shift(2 * DOWN)

        inputs = mid_xor_net[0][0]
        hidden = mid_xor_net[0][1]
        outputs = mid_xor_net[0][2]
        input_edges = mid_xor_net[1][0]
        output_edges = mid_xor_net[1][1]

        foreprop_header = Text("Foreprogation")
        foreprop_header.shift(3 * UP)

        # Transforms to new matricies and new net
        self.play(
            Write(foreprop_header),
            Write(mid_xor_net),
            Write(a1[1:3]),
            Write(w1),
            Write(z1[1:3]),
            Write(b1),
            Write(a2[1:3]),
            Write(w2),
            Write(z2[1:3]),
            Write(b2),
            Write(a3[1:3]),
        )

        self.wait()

        # Equation highlight boxes
        # (this is easier if a bit less clear than transforming equations)
        eqA = get_highlight_box(side_equations[0][0])
        eqZ = get_highlight_box(side_equations[0][1])

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
        a1_scaled = rescale(a1.copy(), store_scale, equation_scale)  # ,h_buff=1.2
        a1_a1_scaled = (
            a1_scaled.copy()
        )  # Re-used later, so we don't use and uncreate the base version

        a1_a1_scaled.center()

        # Writes a1
        self.play(Write(a1_a1_scaled))
        # Stores a1
        self.play(ReplacementTransform(a1_a1_scaled.copy(), a1))
        # Uncreates a1
        self.play(Uncreate(a1_a1_scaled))

        self.wait()

        # ------------------------------------------------------------------------------------
        # z1
        # ------------------------------------------------------------------------------------

        # Highlights equation
        self.play(Write(eqZ))

        # Highlights matricies
        z1_highlight = get_highlight_box(VGroup(a1, w1, b1, z1))
        self.play(ReplacementTransform(a1_highlight, z1_highlight))

        # Highlights 1st hidden layer
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

        bu_scaled = bu.copy()
        bu_scaled.scale(equation_scale)
        z1_bu_scaled = (
            bu_scaled.copy()
        )  # Re-used later, so we don't use and uncreate the base version

        z1_a1_scaled = a1_scaled.copy()

        # z1 calculation
        z1_calculation = VGroup(
            z1_z1_scaled,
            MathTex("="),
            w1_scaled,
            z1_a1_scaled,
            MathTex("+"),
            b1_scaled,
            z1_bu_scaled,
        )
        z1_calculation.arrange()

        # Aligns to side equations
        z1_calculation.move_to(
            [
                side_equations_alignment + z1_calculation.get_width() / 2,
                z1_calculation.get_y(),
                z1_calculation.get_z(),
            ]
        )

        # Pulls a1 into equation
        self.play(ReplacementTransform(a1.copy(), z1_a1_scaled))
        # Pulls w1 into equation
        self.play(ReplacementTransform(w1.copy(), w1_scaled))
        # Pulls b1 into equation
        self.play(ReplacementTransform(b1.copy(), b1_scaled))

        # Writes operations
        self.play(
            Write(z1_z1_scaled),
            Write(z1_calculation[1]),
            Write(z1_calculation[4]),
            Write(z1_bu_scaled),
        )

        # Store z1
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

        # Aligns to side equations
        a2_calculation.move_to(
            [
                side_equations_alignment + a2_calculation.get_width() / 2,
                a2_calculation.get_y(),
                a2_calculation.get_z(),
            ]
        )

        # Pulls z1 into equation
        self.play(ReplacementTransform(z1.copy(), a2_z1_scaled))

        # Writes operations
        self.play(
            Write(a2_a2_scaled), Write(a2_calculation[1:3]), Write(a2_calculation[4])
        )

        self.wait(SCENE_WAIT)

        # Store a2
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

        z2_bu_scaled = bu_scaled.copy()

        z2_calculation = VGroup(
            z2_z2_scaled,
            MathTex("="),
            w2_scaled,
            z2_a2_scaled,
            MathTex("+"),
            b2_scaled,
            z2_bu_scaled,
        )
        z2_calculation.arrange()

        # An admittedly kinda magic number scale, so it can fit on the screen
        z2_calculation.scale(0.8)

        # Aligns to side equations
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
            Write(z2_z2_scaled),
            Write(z2_calculation[1]),
            Write(z2_calculation[4]),
            Write(z2_bu_scaled),
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

        # Aligns to side equations
        a3_calculation.move_to(
            [
                side_equations_alignment + a3_calculation.get_width() / 2,
                a3_calculation.get_y(),
                a3_calculation.get_z(),
            ]
        )

        self.play(ReplacementTransform(z2.copy(), a3_z2_scaled))

        self.play(
            Write(a3_scaled),
            Write(a3_calculation[1:3]),
            Write(a3_calculation[4]),
        )

        # Stores a3
        self.play(ReplacementTransform(a3_scaled.copy(), a3))

        self.wait(SCENE_WAIT)

        self.play(Uncreate(a3_calculation))

        # Done
        # ------------------------------------------------------------------------------------

        self.play(Write(Text("Contratz.")))

        self.wait()

    def construct(self):
        # Scene 1: Title screen
        # -----------------------------
        self.play_intro()

        # Scene 2: SIMD vs SISD
        # -----------------------------
        self.play_simd()

        # Scene 3: Batch foreprop equations
        # -----------------------------
        side_equations = self.play_equations()

        # Scene 4: Batch foreprop
        # -----------------------------
        self.play_batch_forwardpropagation(side_equations)
