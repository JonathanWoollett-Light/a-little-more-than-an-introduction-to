from manimlib.imports import *

# Episodes are numbered with major and minor numbers (e.g. 1.x covers dense nets (func names being 1_0,1_1,etc.), 2.x covers conv nets)
# Utility functions are defined just before the 1st episode in which they are used

# Gets title screen
def get_title_screen(episodeNumber,episodeDescription):
    super_title = TextMobject("A little more than an introduction to:")
    super_title.scale(0.75)
    title = TextMobject("Neural Networks")
    title.scale(2)
    subtitle = TextMobject("Episode "+str(episodeNumber)+": "+episodeDescription)
    subtitle.scale(0.75)
    title_scene = VGroup(super_title,title,subtitle)
    title_scene.arrange(DOWN,buff=1)

    return title_scene

# Gets an xor net
def get_xor_net(text_scale, vertical_spacing, horizontal_spacing):
        inputs = VGroup(*[Circle(radius=0.15,stroke_color=WHITE,stroke_width=1) for i in range(0,2)])
        inputs.arrange(DOWN,buff=vertical_spacing)
        hidden = VGroup(*[Circle(radius=0.15,stroke_color=WHITE,stroke_width=1) for i in range(0,3)])
        hidden.arrange(DOWN,buff=vertical_spacing)
        outputs = VGroup(
            VGroup(Circle(radius=0.15,stroke_color=WHITE,stroke_width=1),TextMobject("False")),
            VGroup(Circle(radius=0.15,stroke_color=WHITE,stroke_width=1),TextMobject("True"))
        )
        for group in outputs:
            group[1].scale(text_scale)
            group.arrange()
        outputs.arrange(DOWN,buff=vertical_spacing)

        neurons = VGroup(inputs,hidden,outputs)
        neurons.arrange(buff=horizontal_spacing)

        input_edges = VGroup(*[Line(n1.get_center(),n2[0].get_center(),stroke_width=0.5) for n1 in inputs for n2 in hidden])
        output_edges = VGroup(*[Line(n1.get_center(),n2[0].get_center(),stroke_width=0.5) for n1 in hidden for n2 in outputs])

        connections = VGroup(input_edges,output_edges)

        return VGroup(neurons,connections)

# Creates a box of a bunch of equations
def get_equations(equations,wheres=[],buffer=1,scale=0.5,where_scale=0.8):
    equation_box = [TexMobject(str(i+1)+r". \hspace{6pt}",eqStr) for (i,eqStr) in enumerate(equations)]

    if len(wheres) > 0:
        wheresList = [r"Where: \hspace{6pt}"]
        for (i,eqStr) in enumerate(wheres):
            wheresList.append(eqStr)
            if i != len(wheres)-1: # For all but last element add `,` after
                wheresList.append(", ")
        
        wheresTex = TexMobject(*wheresList)
        wheresTex.scale(where_scale)
        equation_box.append(wheresTex)

    equation_box = VGroup(*equation_box)

    equation_box.arrange(DOWN,buff=0.75)

    align_pos_x = equation_box.get_center()[0]-equation_box.get_width()/2 + buffer
    for eq in equation_box:
        eq.move_to([align_pos_x+eq.get_width()/2,eq.get_y(),eq.get_z()])

    border = Rectangle(height=equation_box.get_height()+1,width=equation_box.get_width()+1)
    border.move_to(equation_box.get_center())

    equation_box = VGroup(equation_box,border)
    equation_box.scale(scale)
    equation_box.center()

    return equation_box

# Gets yellow box around thing
def get_highlight_box(x,buffer=0.3,stroke_width=2):
    box = Rectangle(stroke_width=stroke_width,color=YELLOW,height=x.get_height()+buffer,width=x.get_width()+buffer)
    box.move_to(x.get_center())
    return box

# Puts all centers of components of y vertically inline with centers of components of x.
# Simply put, horziontally aligns components of y with components of x.
def align_horizontally(x,y):
    for (xc,yc) in zip(x,y):
        yc.move_to([xc.get_x(),yc.get_y(),yc.get_z()])

SCENE_WAIT = 30 # Seconds to wait (gives space for cropping to fit audio in editing)

# Foreprop
class ep1_0(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.0,"Forepropagation")

        self.add(title_scene)

        self.wait(SCENE_WAIT)

        self.play(Uncreate(title_scene))

    def play_note_on_3b3b1(self):
        text = TextMobject("First check out 3Blue1Browns neural network series before watching this.")
        text.scale(0.5)
        img = ImageMobject("3b1b nets.png")
        img.scale(1.5)

        text.next_to(img,TOP)
        text.shift(DOWN / 2)

        self.play(Write(text),FadeIn(img))

        self.wait(SCENE_WAIT)

        self.play(Uncreate(text),Uncreate(img))

    def play_mnist_net(self,scale=0.5):
        top = [Circle(radius=0.15,stroke_color=WHITE,stroke_width=1) for i in range(0,10)]
        bottom = [Circle(radius=0.15,stroke_color=WHITE,stroke_width=1) for i in range(0,10)]
        inputs = VGroup(*top,TexMobject("\\vdots"),*bottom)
        inputs.arrange(DOWN)
        inputs = VGroup(TextMobject("784"),Brace(inputs,LEFT),inputs)
        inputs.arrange()

        hidden1 = VGroup(*[Circle(radius=0.15,stroke_color=WHITE,stroke_width=1) for i in range(0,16)])
        hidden1.arrange(DOWN)
        hidden2 = hidden1.copy()

        outputs = VGroup(*[VGroup(Circle(radius=0.15,stroke_color=WHITE,stroke_width=1),TextMobject(i)) for i in range(0,10)])
        for group in outputs:
            group.arrange()
        
        outputs.arrange(DOWN)

        neurons = VGroup(inputs,hidden1,hidden2,outputs)
        neurons.arrange(buff=2)

        top_edges = VGroup(*[Line(n1.get_center(),n2.get_center(),stroke_width=0.2) for n1 in top for n2 in hidden1])
        bottom_edges = VGroup(*[Line(n1.get_center(),n2.get_center(),stroke_width=0.2) for n1 in bottom for n2 in hidden1])

        hidden_edges = VGroup(*[Line(n1.get_center(),n2.get_center(),stroke_width=0.2) for n1 in hidden1 for n2 in hidden2])

        output_edges = VGroup(*[Line(n1.get_center(),n2[0].get_center(),stroke_width=0.2) for n1 in hidden2 for n2 in outputs])

        connections = VGroup(top_edges,bottom_edges,hidden_edges,output_edges)
        #net.scale(0.4)

        mnist_net = VGroup(neurons,connections)        
        mnist_net.scale(scale)

        mnist_text = TextMobject("MNIST")
        scene = VGroup(mnist_text,mnist_net)
        scene.arrange(DOWN)

        self.play(Write(mnist_text))
        self.play(Write(neurons))
        self.play(Write(connections))

        return (mnist_net,mnist_text)

    def play_xor_net(self,mnist_net,mnist_text,scale=0.8,shift=3.5,arrow_spacing=0.05):
        xor_net = get_xor_net(1,0.75,2)
        xor_net.move_to(mnist_net.get_center())
        xor_net.scale(scale)

        xor_text = TextMobject("XOR")
        xor_text.move_to(mnist_text.get_center())

        xor = VGroup(xor_text,xor_net)
        xor.shift(shift*RIGHT)

        self.play(
            Transform(mnist_net,mnist_net.copy().shift(shift*LEFT)),
            Transform(mnist_text,mnist_text.copy().shift(shift*LEFT))
        )

        arrow = Arrow(
            ORIGIN+shift*LEFT+[arrow_spacing+mnist_net.get_width()/2,0,0],
            ORIGIN+shift*RIGHT-[arrow_spacing+xor_net.get_width()/2,0,0]
        )
        self.play(Write(arrow))
        self.play(Write(xor_text))
        self.play(Write(xor_net))

        self.wait(SCENE_WAIT)

        self.play(
            Uncreate(mnist_net),
            Uncreate(mnist_text),
            Uncreate(arrow)
        )

        return (xor_net,xor_text)

    def play_xor_dataset(self,xor_net,xor_text):
        inputs = VGroup(
            Matrix([[0,0]],h_buff=0.5),
            Matrix([[1,0]],h_buff=0.5),
            Matrix([[0,1]],h_buff=0.5),
            Matrix([[1,1]],h_buff=0.5)
        )
        inputs.arrange(DOWN)
        inputs = VGroup(TextMobject("Inputs"),inputs)
        inputs.arrange(DOWN)

        false = VGroup(Matrix([[1,0]],h_buff=0.5),TextMobject("False"))
        true = VGroup(Matrix([[0,1]],h_buff=0.5),TextMobject("True"))

        outputs = VGroup(
            false.copy(),
            true.copy(),
            true.copy(),
            false.copy()
        )
        for output in outputs:
            output.arrange()
        outputs.arrange(DOWN)
        outputs = VGroup(TextMobject("Outputs"),outputs)
        outputs.arrange(DOWN)

        labels = Matrix([0,1,1,0],v_buff=1.15)
        labels = VGroup(TextMobject("Labels"),labels)
        labels.arrange(DOWN)

        moved_xor = xor_net.copy()

        scene = VGroup(inputs,outputs,labels,moved_xor)
        scene.arrange(buff=2.5)
        scene.scale(0.5)

        self.play(Transform(xor_text,xor_text.copy().move_to(ORIGIN+[0,xor_text.get_y(),0])))

        self.play(Transform(xor_net,moved_xor))

        self.play(Write(inputs))

        self.play(Write(outputs))

        self.play(Write(labels))

        self.wait(SCENE_WAIT)

        self.play(
            Uncreate(scene[0:3]),
            Uncreate(xor_text)
        )

    def play_xor_values(self,xor_net):
        # Sets up wide XOR net
        # -----------------------------
        wide_xor_net = get_xor_net(0.5,0.25,4)

        # Define some useful aliases
        # -----------------------------
        inputs = wide_xor_net[0][0]
        hidden = wide_xor_net[0][1]
        outputs = wide_xor_net[0][2]

        input_edges = wide_xor_net[1][0]
        output_edges = wide_xor_net[1][1]

        # Sets up vague value matricies
        # -----------------------------
        z1 = TexMobject(r"""
        \begin{bmatrix}
            z_{1,1} \\[6pt] z_{1,2} \\[6pt] z_{1,3}
        \end{bmatrix}
        """)
        z2 = TexMobject(r"""
        \begin{bmatrix}
            z_{2,1} \\[6pt] z_{2,2}
        \end{bmatrix}
        """)

        a1 = TexMobject(r"""
        \begin{bmatrix}
            a_{1,1} \\[6pt] a_{1,2}
        \end{bmatrix}
        """)
        a2 = TexMobject(r"""
        \begin{bmatrix}
            a_{2,1} \\[6pt] a_{2,2} \\[6pt] a_{2,3}
        \end{bmatrix}
        """)
        a3 = TexMobject(r"""
        \begin{bmatrix}
            a_{3,1} \\[6pt] a_{3,2}
        \end{bmatrix}
        """)

        w1 = TexMobject(r"""
        \begin{bmatrix}
            w_{1,1,1} & w_{1,1,2} \\[6pt]
            w_{1,2,1} & w_{1,2,2} \\[6pt]
            w_{1,3,1} & w_{1,3,2}
        \end{bmatrix}
        """,color=RED)
        w2 = TexMobject(r"""
        \begin{bmatrix}
            w_{2,1,1} & w_{2,1,2} & w_{2,1,3} \\[6pt]
            w_{2,2,1} & w_{2,2,2} & w_{2,2,3}
        \end{bmatrix}
        """,color=RED)

        b1 = TexMobject(r"""
        \begin{bmatrix}
            b_{1,1} \\[6pt] b_{1,2} \\[6pt] b_{1,3}
        \end{bmatrix}
        """,color=BLUE)
        b2 = TexMobject(r"""
        \begin{bmatrix}
            b_{2,1} \\[6pt] b_{2,2}
        \end{bmatrix}
        """,color=BLUE)

        # Sets groups for hidden and output layer neurons
        # -----------------------------
        n1 = VGroup(b1,z1,a2)
        n1.arrange()
        n2 = VGroup(b2,z2,a3)
        n2.arrange()

        # Scale and align all matricies
        # -----------------------------
        values = VGroup(a1,w1,n1,w2,n2)
        values.scale(0.4)
        values.arrange()

        # Sets scene arrangement
        # -----------------------------
        title = TextMobject("What values are we looking at?")
        scene = VGroup(title,values,wide_xor_net)
        scene.arrange(DOWN,buff=1)

        # Horizontally aligns matricies over respective network sections
        # -----------------------------
        # Doing horizontal alignment manually since can't figure out `align_to`
        a1.move_to([inputs.get_x(),a1.get_y(),a1.get_z()])
        n1.move_to([hidden.get_x(),n1.get_y(),n1.get_z()])
        n2.move_to([outputs[0][0].get_x(),n2.get_y(),n2.get_z()])

        w1.move_to([input_edges.get_x(),w1.get_y(),w1.get_z()])
        w2.move_to([output_edges.get_x(),w2.get_y(),w2.get_z()])

        # Transforms from old xor net to new xor net (which is lower and wider)
        # -----------------------------
        self.play(ReplacementTransform(xor_net,wide_xor_net))

        # Writes title
        # -----------------------------
        self.play(Write(scene[0]))

        self.play(ReplacementTransform(inputs.copy(),a1))

        outputGroup = VGroup(outputs[0][0],outputs[1][0])
        # Illutrates b's, z's and a's
        self.play(
            ReplacementTransform(hidden.copy(),n1),
            ReplacementTransform(outputGroup.copy(),n2)
        )
        # Illutrates w's
        self.play(
            ReplacementTransform(input_edges.copy(),w1),
            ReplacementTransform(output_edges.copy(),w2)
        )

        self.wait(SCENE_WAIT)

        self.play(Uncreate(title))

        return (values,wide_xor_net)

    def play_equations(self,values,wide_xor_net):
        # Gets small XOR net
        mid_xor_net = get_xor_net(0.5,0.25,2)

        # Shifts matricies up
        moved_values = values.copy()
        moved_values.shift(1.5*UP)

        # Shifts net down
        mid_xor_net.move_to(wide_xor_net.get_center())
        mid_xor_net.shift(1*DOWN)

        # Transforms to new matricies and new net
        self.play(
            ReplacementTransform(wide_xor_net,mid_xor_net),
            ReplacementTransform(values,moved_values)
        )

        side_equations = get_equations(equations=[
            r"a^{l+1} = A(z^l)",
            r"z^l = w^l a^l + b^l"
        ])

        title = TextMobject("Foreprop Equations")
        title.move_to(side_equations.get_center()+3*UP)

        self.play(Write(title))

        self.play(Write(side_equations))

        self.wait(SCENE_WAIT)

        self.play(ReplacementTransform(side_equations,side_equations.copy().shift(5*LEFT)))

        self.play(Uncreate(title))

        return (side_equations,moved_values,mid_xor_net)

    def play_forepropagation(self,moved_values,net,side_equations,store_scale=0.5,equation_scale=0.7):
        # Define some useful aliases
        # -----------------------------
        side_equations_alignment = side_equations.get_x() + side_equations.get_width()/2 + 0.5

        wide_xor_net = net

        inputs = wide_xor_net[0][0]
        hidden = wide_xor_net[0][1]
        outputs = wide_xor_net[0][2]
        input_edges = wide_xor_net[1][0]
        output_edges = wide_xor_net[1][1]

        # Sets up matricies with values
        a1 = Matrix(["0","1"],h_buff=1.2)
        a2 = Matrix(["0.47...","0.62...","0.52..."],h_buff=1.2)
        a3 = Matrix(["0.62...","0.53..."],h_buff=1.2)

        z1 = Matrix(["-0.1","0.5","0.1"],h_buff=1.2)
        z2 = Matrix(["0.49...","0.12..."],h_buff=1.5)

        w1 = TexMobject(r"""
        \begin{bmatrix}
            -0.2 & 0.2 \\[6pt]
            0.1 & 0.2 \\[6pt]
            0.5 & -0.5
        \end{bmatrix}
        """,color=RED)
        w2 = TexMobject(r"""
        \begin{bmatrix}
            -0.2 & 0.2 & 0.5 \\[6pt]
            0.1 & 0.2 & 0.3
        \end{bmatrix}
        """,color=RED)

        b1 = TexMobject(r"""
        \begin{bmatrix}
            -0.3 \\[6pt] 0.3 \\[6pt] 0.6
        \end{bmatrix}
        """,color=BLUE)
        b2 = TexMobject(r"""
        \begin{bmatrix}
            0.2 \\[6pt] -0.2
        \end{bmatrix}
        """,color=BLUE)

        # Sets up matricies
        net_values_precise = VGroup(a1,w1,b1,z1,a2,w2,b2,z2,a3)
        net_values_precise.scale(store_scale) # Scales up matricies
        net_values_precise.arrange()
        net_values_precise.move_to(moved_values.get_center())

        # ------------------------------------------------------------------------------------
        # Sets up highlights boxes
        # ------------------------------------------------------------------------------------

        eqZ = get_highlight_box(side_equations[0][1])
        eqA = get_highlight_box(side_equations[0][0])

        foreprop_header = TextMobject("Foreprogation")
        foreprop_header.shift(3*UP)

        # Transforms to precise values (leaving out a and z values)
        # Done by each matrix to make it clearer
        self.play(
            Write(foreprop_header),
            ReplacementTransform(moved_values[0],a1[1:3]),
            ReplacementTransform(moved_values[1],w1),
            ReplacementTransform(moved_values[2][0],z1[1:3]),
            ReplacementTransform(moved_values[2][1],b1),
            ReplacementTransform(moved_values[2][2],a2[1:3]),
            ReplacementTransform(moved_values[3],w2),
            ReplacementTransform(moved_values[4][0],z2[1:3]),
            ReplacementTransform(moved_values[4][1],b2),
            ReplacementTransform(moved_values[4][2],a3[1:3]),
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
        a1_scaled = rescale(a1.copy(),store_scale,equation_scale)
        a1_a1_scaled = a1_scaled.copy() # Re-used later, so we don't use and uncreate the base version
        
        a1_a1_scaled.center()

        # Writes a1
        self.play(Write(a1_a1_scaled))
        # Stores a1
        self.play(ReplacementTransform(a1_a1_scaled.copy(),a1))
        
        self.wait(SCENE_WAIT)
        
        # Uncreates a1
        self.play(Uncreate(a1_a1_scaled))

        # ------------------------------------------------------------------------------------
        # z1
        # ------------------------------------------------------------------------------------

        # Highlights equation
        self.play(Write(eqZ))

        # Highlights matricies
        z1_highlight = get_highlight_box(VGroup(a1,w1,b1,z1))
        self.play(ReplacementTransform(a1_highlight,z1_highlight))

        # Highlights input edges
        inputs.set_color(WHITE)
        input_edges.set_color(YELLOW)
        hidden.set_color(YELLOW)
        self.play(
            Write(input_edges), # Re-writes edges
            Write(hidden) # Re-writes to update
        )

        z1_scaled = rescale(z1.copy(),store_scale,equation_scale)
        z1_z1_scaled = z1_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        w1_scaled = rescale(w1.copy(),store_scale,equation_scale)

        b1_scaled = rescale(b1.copy(),store_scale,equation_scale)

        z1_a1_scaled = a1_scaled.copy()

        # Sets z1 calculation
        z1_calculation = VGroup(
            z1_z1_scaled,
            TexMobject("="),
            z1_a1_scaled,
            w1_scaled,
            TexMobject("+"),
            b1_scaled
        )
        z1_calculation.arrange()

        # Pulls a1 into equation
        self.play(ReplacementTransform(a1.copy(),z1_a1_scaled))
        # Pulls w1 into equation
        self.play(ReplacementTransform(w1.copy(),w1_scaled))
        # Pulls b1 into equation
        self.play(ReplacementTransform(b1.copy(),b1_scaled))

        # Writes operations
        self.play(
            Write(z1_z1_scaled),
            Write(z1_calculation[1]),
            Write(z1_calculation[4])
        )

        # Stores z1
        self.play(ReplacementTransform(z1_z1_scaled.copy(),z1))

        self.wait(SCENE_WAIT)

        # Clears z1 calculation
        self.play(Uncreate(z1_calculation))

        # ------------------------------------------------------------------------------------
        # a2
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqZ = retainTransform(self,eqZ,eqA)

        # Highlights matricies
        a2_highlight = get_highlight_box(VGroup(z1,a2))
        self.play(ReplacementTransform(z1_highlight,a2_highlight))

        a2_scaled = rescale(a2.copy(),store_scale,equation_scale)
        a2_a2_scaled = a2_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        a2_z1_scaled = z1_scaled.copy()

        a2_calculation = VGroup(
            a2_a2_scaled,
            TexMobject("="),
            TexMobject(r"\sigma \Big("),
            a2_z1_scaled,
            TexMobject(r"\Big)")
        )
        a2_calculation.arrange()

        # Pulls z1 into equation
        self.play(ReplacementTransform(z1.copy(),a2_z1_scaled))

        # Writes operations
        self.play(
            Write(a2_a2_scaled),
            Write(a2_calculation[1:3]),
            Write(a2_calculation[4])
        )

        # Stores a2
        self.play(ReplacementTransform(a2_a2_scaled.copy(),a2))

        self.wait(SCENE_WAIT)

        # Clears equation
        self.play(Uncreate(a2_calculation))

        # ------------------------------------------------------------------------------------
        # z2
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqA = retainTransform(self,eqA,eqZ)

        # Highlights matricies
        z2_highlight = get_highlight_box(VGroup(a2,w2,b2,z2))
        self.play(ReplacementTransform(a2_highlight,z2_highlight))

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
            Write(outputs)
        )

        w2_scaled = rescale(w2.copy(),store_scale,equation_scale)

        z2_a2_scaled = a2_scaled.copy()

        b2_scaled = rescale(b2.copy(),store_scale,equation_scale)
        # Could scale this to match size of `input_weight_result`, but honestly who cares, this just adds unneccessary complexitity

        z2_scaled = rescale(z2.copy(),store_scale,equation_scale)
        z2_z2_scaled = z2_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        z2_calculation = VGroup(
            z2_z2_scaled,
            TexMobject("="),
            w2_scaled,
            z2_a2_scaled,
            TexMobject("+"),
            b2_scaled
        )
        z2_calculation.arrange()

        # Aligns to side equations.
        #  Only needed here bc this is the only equation in this video
        #  which doesn't fit otherwise.
        z2_calculation.move_to([
            side_equations_alignment + z2_calculation.get_width()/2,
            z2_calculation.get_y(),
            z2_calculation.get_z()
        ])

        # Pulls input weights into equation
        self.play(ReplacementTransform(a2.copy(),z2_a2_scaled))
        # Pulls input weights into equation
        self.play(ReplacementTransform(w2.copy(),w2_scaled))
        # Pulls biases into equation
        self.play(ReplacementTransform(b2.copy(),b2_scaled))
        # Writes operations
        self.play(
            Write(z2_z2_scaled),
            Write(z2_calculation[1]),
            Write(z2_calculation[4])
        )
        # Store result into matricies
        self.play(ReplacementTransform(z2_z2_scaled.copy(),z2))
        # Clears equation
        self.play(Uncreate(z2_calculation))

        # ------------------------------------------------------------------------------------
        # a3
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqZ = retainTransform(self,eqZ,eqA)

        a3_highlight = get_highlight_box(VGroup(z2,a3))
        self.play(ReplacementTransform(z2_highlight,a3_highlight))

        a3_scaled = rescale(a3.copy(),store_scale,equation_scale)

        a3_z2_scaled = z2_scaled.copy()

        a3_calculation = VGroup(
            a3_scaled,
            TexMobject("="),
            TexMobject(r"\sigma \Big("),
            a3_z2_scaled,
            TexMobject(r"\Big)")
        )
        a3_calculation.arrange()

        # Pulls z2 into calculation
        self.play(ReplacementTransform(z2.copy(),a3_z2_scaled))
        
        self.play(
            Write(a3_scaled),
            Write(a3_calculation[1:3]),
            Write(a3_calculation[4]),
        )

        # Stores a3
        self.play(ReplacementTransform(a3_scaled.copy(),a3))

        self.play(Uncreate(a3_calculation))

        # Done
        # ------------------------------------------------------------------------------------

        self.play(Write(TextMobject("Done.")))

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
        self.play_xor_dataset(xor_net,xor_text)

        # Scene 6: Values in net
        # -----------------------------
        values, net = self.play_xor_values(xor_net)

        # Scene 7: Foreprop equations
        # -----------------------------
        equations, values, net = self.play_equations(values,net)
        
        # Scene 8: Does foreprop
        # -----------------------------
        self.play_forepropagation(values,net,equations)

# Backprop
class ep1_1(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.1,"Backpropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_equations(self):
        side_equations = get_equations(equations=[
            r"\delta^L = \nabla_a C \odot A'(z^L)",
            r"\delta^l = (w^{l+1})^T \delta^{l+1} \odot A'(z^l)",
            r"\frac{\partial C}{\partial b^l} = \delta^l",
            r"\frac{\partial C}{\partial w^l} = \delta^l (a^l)^T"
        ], wheres=[r"\delta^l = \frac{\partial C}{\partial z^l}"],scale=0.3)

        title = TextMobject("Backpropagation")
        title.move_to(side_equations.get_center()+3*UP)

        self.play(Write(title))
        self.wait(3)
        self.play(Write(side_equations))
        self.wait(3)

        self.play(ReplacementTransform(side_equations,side_equations.copy().shift(5*LEFT)))

        return (title,side_equations)

    def play_backpropagation(self,title,side_equations,store_scale=0.3):

        # Sets up matricies with values
        # ----------------------------------------------------------
        a1 = Matrix(["0","1"],h_buff=1.2)
        a2 = Matrix(["0.47...","0.62...","0.52..."],h_buff=1.2)
        a3 = Matrix(["0.62...","0.53..."],h_buff=1.2)

        z1 = Matrix(["-0.1","0.5","0.1"],h_buff=1.2)
        z2 = Matrix(["0.29...","0.33..."],h_buff=1.5)

        w1 = TexMobject(r"""
        \begin{bmatrix}
            -0.2 & 0.2 \\[6pt]
            0.1 & 0.2 \\[6pt]
            0.5 & -0.5
        \end{bmatrix}
        """,color=RED)
        w1e = Matrix([
            ["0","-0.01..."],
            ["0","0.00..."],
            ["0","0.00..."]
        ],h_buff=2).set_color(GREEN)
        w2 = TexMobject(r"""
        \begin{bmatrix}
            -0.2 & 0.2 & 0.5 \\[6pt]
            0.1 & 0.2 & 0.3
        \end{bmatrix}
        """,color=RED)
        w2e = Matrix([
            ["0.06...","0.09...","0.07..."],
            ["-0.05...","-0.07...","-0.06..."]
        ],h_buff=2).set_color(GREEN)

        b1 = TexMobject(r"""
        \begin{bmatrix}
            -0.3 \\[6pt] 0.3 \\[6pt] 0.6
        \end{bmatrix}
        """,color=BLUE)
        b1e = Matrix(["-0.01...","0.00...","0.00..."]).set_color(GREEN)
        b2 = TexMobject(r"""
        \begin{bmatrix}
            0.2 \\[6pt] -0.2
        \end{bmatrix}
        """,color=BLUE)
        b2e = Matrix(["0.14...","-0.11..."]).set_color(GREEN)

        n1 = VGroup(w1e,b1,b1e,z1,a2)
        n2 = VGroup(w2e,b2,b2e,z2,a3)
        
        # Scales all matricies
        net_values_precise = VGroup(a1,w1,w1e,b1,b1e,z1,a2,w2,w2e,b2,b2e,z2,a3)
        net_values_precise.arrange()
        net_values_precise.scale(store_scale) # Scales down matricies

        title_and_values = VGroup(title.copy(),net_values_precise)
        title_and_values.arrange(DOWN)

        # Sets net
        # -----------------------------
        mid_xor_net = get_xor_net(0.5,0.25,2)

        # Sets intial scene
        # ----------------------------------------------------------
        a3_scaled = a3.copy()
        a3_scaled.scale(1/store_scale)

        equation = TexMobject(r"\delta^L", "=", r"\nabla_a C", r"\odot", r"A'(z^L)")

        current = VGroup(a3_scaled,equation)
        current.arrange(DOWN)

        scene = VGroup(title_and_values,current,mid_xor_net)
        scene.arrange(DOWN,buff=1.25)

        mid_xor_net.shift(0.2*UP)

        net_values_precise_excluding_errors = VGroup(a1,w1,w1e[1:3],z1,b1,b1e[1:3],a2,w2,w2e[1:3],z2,b2,b2e[1:3],a3)

        self.play(ReplacementTransform(title,title_and_values[0]))
        self.play(
            Write(net_values_precise_excluding_errors),
            Write(a3_scaled),
            Write(mid_xor_net)
        )
        self.wait(10)

        # Sets highlight boxes
        # -----------------------------
        
        # Sets matrix highlight boxes
        n1Selected = get_highlight_box(n1,buffer=0.2)
        n2Selected = get_highlight_box(n2,buffer=0.2)

        # Sets equation highlight boxes
        outErrorEqSelected = get_highlight_box(side_equations[0][0])
        errorEqSelected = get_highlight_box(side_equations[0][1])
        bEqSelected = get_highlight_box(side_equations[0][2])
        wEqSelected = get_highlight_box(side_equations[0][3])

        # Sets output neuron error
        # ----------------------------------------------------------

        # Sets equation hightlight
        self.play(Write(outErrorEqSelected))

        target = Matrix(["0","1"],h_buff=1)

        # Result
        output_cz_derivative = Matrix(["0.14...","-0.11..."],h_buff=1.75)

        # Sets calculation
        calculation = VGroup(
            output_cz_derivative.copy(),
            TexMobject("="),
            VGroup(a3_scaled.copy(),TexMobject("-"),target),
            TexMobject(r"\odot"),
            VGroup(TexMobject(r"\Bigg("),a3_scaled.copy(),TexMobject(r"\odot"),TexMobject(r"\bigg(1-"),a3_scaled.copy(),TexMobject(r"\bigg)"),TexMobject(r"\Bigg)"))
        )
        calculation.scale(0.4)
        calculation[2].arrange(buff=0.1)
        calculation[4].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        side_equations_alignment = side_equations.get_x() + side_equations.get_width()/2 + 0.5
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])

        # Aligns equation to calculation
        align_horizontally(calculation,equation)

        # Highlights output
        mid_xor_net[0][2][0][0].set_color(YELLOW)
        mid_xor_net[0][2][1][0].set_color(YELLOW)
        mid_xor_net[1][1].set_color(YELLOW)
        self.play(
            Write(n2Selected),
            Write(mid_xor_net[0][2][0][0]),
            Write(mid_xor_net[0][2][1][0]),
            Write(mid_xor_net[1][1])
        )

        self.play(ReplacementTransform(a3_scaled,calculation[2][0]))
        self.play(ReplacementTransform(a3_scaled.copy(),calculation[4][1]))
        self.play(ReplacementTransform(calculation[4][1].copy(),calculation[4][4]))

        self.play(
            Write(calculation[1]),
            Write(calculation[2][1]),
            Write(calculation[2][2]),
            Write(calculation[3]),
            Write(calculation[4][0]),
            Write(calculation[4][2:4]),
            Write(calculation[4][5:7])
        )

        self.play(ReplacementTransform(side_equations[0][0][1].copy(),equation))
        self.wait()
        self.play(Write(calculation[0]))
        self.wait()

        
        sigmoid_derivative = TexMobject(r"\sigma '(z)",r"= \sigma (z) (1- \sigma (z))","= a(1-a)")
        sigmoid_derivative.scale(0.6)
        sigmoid_derivative[2].move_to([
            sigmoid_derivative[1].get_x()-sigmoid_derivative[1].get_width()/2+sigmoid_derivative[2].get_width()/2,
            sigmoid_derivative.get_y()-1.2*sigmoid_derivative.get_height(),
            sigmoid_derivative.get_z()
        ])
        sigmoid_derivative.move_to(equation[4].get_center())

        equation4_holder = equation[4].copy()
        self.play(ReplacementTransform(equation[4],sigmoid_derivative))
        self.wait(3)
        self.play(ReplacementTransform(sigmoid_derivative,equation4_holder))
        self.wait(3)

        # Left bit
        output_az_derivative = Matrix(["0.62...","-0.46..."],h_buff=1.75)
        output_az_derivative.scale(0.4)
        output_az_derivative.move_to(calculation[2].get_center())
        self.play(ReplacementTransform(calculation[2],output_az_derivative))
        self.wait()

        # Right bit
        output_ca_derivative_halfway = Matrix(["-0.37...","-0.46..."],h_buff=1.75)
        output_ca_derivative_halfway.scale(0.4)
        output_ca_derivative_halfway.move_to(calculation[4][3:6].get_center())
        self.play(ReplacementTransform(calculation[4][3:6],output_ca_derivative_halfway))
        self.wait()

        output_ca_derivative = Matrix(["0.23...","0.24.."],h_buff=1.75)
        output_ca_derivative.scale(0.4)
        output_ca_derivative.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(VGroup(calculation[4],output_ca_derivative_halfway),output_ca_derivative))
        self.wait()

        self.play(
            Uncreate(calculation[1]),
            Uncreate(calculation[3]),
            Uncreate(output_az_derivative),
            Uncreate(output_ca_derivative),
            Uncreate(equation[0:4]),
            Uncreate(equation4_holder)
        )

        # Sets output bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        outErrorEqSelected = retainTransform(self,outErrorEqSelected,bEqSelected)

        holder = calculation[0]

        b2e_scaled = b2e.copy()
        b2e_scaled.scale(1/store_scale)

        calculation = VGroup(b2e_scaled,TexMobject("="),output_cz_derivative.copy())
        calculation.scale(0.4)
        calculation.arrange(buff=0.5)
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])

        self.play(ReplacementTransform(holder,calculation[2]))

        old_question_center = equation.get_center()
        equation = TexMobject(r"\frac{\partial C}{\partial b^l}", "=", r"\delta^l")
        equation.move_to(old_question_center)

        # Horizontally aligns equation components to calculation components
        align_horizontally(calculation,equation)

        self.play(ReplacementTransform(side_equations[0][2][1].copy(),equation))
        self.wait()
        self.play(Write(calculation[0:2]))

        self.play(ReplacementTransform(calculation[0].copy(),b2e))

        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(equation)
        )

        # Sets output weight error
        # ----------------------------------------------------------
        
        # Sets equation hightlight
        bEqSelected = retainTransform(self,bEqSelected,wEqSelected)

        w2e_scaled = w2e.copy()
        w2e_scaled.scale(1/store_scale)

        a2_scaled = a2.copy()
        a2_scaled.scale(1/store_scale)

        holder = calculation[2]
        calculation = VGroup(
            w2e_scaled,
            TexMobject("="),
            output_cz_derivative.copy(),
            VGroup(TexMobject(r"\Bigg("),a2_scaled,TexMobject(r"\Bigg)^T"))
        )
        calculation.scale(0.4)
        calculation[3].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])
        self.play(ReplacementTransform(holder,calculation[2]))

        old_question_center = equation.get_center()
        equation = TexMobject(r"\frac{\partial C}{\partial w^l}" ,"=", r"\delta_l", r"(a^{l-1})^T")
        equation.move_to(old_question_center)

        align_horizontally(calculation,equation)

        self.play(ReplacementTransform(side_equations[0][3][1].copy(),equation))

        self.play(ReplacementTransform(a2.copy(),calculation[3][1]))

        self.play(
            Write(calculation[0:2]),
            Write(calculation[3][0]),
            Write(calculation[3][2])
        )

        self.play(ReplacementTransform(calculation[0].copy(),w2e))
        
        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(calculation[3]),
            Uncreate(equation[0:2]),
            Uncreate(equation[3])
        )

        self.wait(1) # Explanation before repeat

        self.play(Uncreate(equation[2]))

        # Sets hidden neuron error
        # ----------------------------------------------------------
        
        # Sets equation hightlight
        wEqSelected = retainTransform(self,wEqSelected,errorEqSelected)

        old_question_center = equation.get_center()
        equation = TexMobject(r"\delta^l", "=", r"(w^{l+1})^T", r"\delta^{l+1}", r"\odot", r"A'(z^l)")
        equation.move_to(old_question_center)

        # Result
        hidden_cz_derivative = Matrix(["-0.01...","0.00...","0.00..."],h_buff=1.75)

        w2_scaled = w2.copy()
        w2_scaled.scale(1/store_scale)

        a2_scaled = a2.copy()
        a2_scaled.scale(1/store_scale)

        holder = calculation[2] # delta_l-1

        # Sets calculation
        calculation = VGroup(
            hidden_cz_derivative.copy(),
            TexMobject("="),
            VGroup(TexMobject(r"\Bigg("),w2_scaled,TexMobject(r"\Bigg)^T")),
            output_cz_derivative.copy(),
            TexMobject(r"\odot"),
            VGroup(TexMobject(r"\Bigg("),a2_scaled.copy(),TexMobject(r"\odot"),TexMobject(r"\bigg(1-"),a2_scaled.copy(),TexMobject(r"\bigg)"),TexMobject(r"\Bigg)"))
        )
        calculation.scale(0.4)
        calculation[2].arrange(buff=0.1)
        calculation[5].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])

        # Aligns equation to calculation
        align_horizontally(calculation,equation)

        mid_xor_net[0][2][0][0].set_color(WHITE)
        mid_xor_net[0][2][1][0].set_color(WHITE)
        mid_xor_net[1][1].set_color(WHITE)
        # Highlights output
        mid_xor_net[0][1].set_color(YELLOW)
        mid_xor_net[1][0].set_color(YELLOW)
        self.play(
            ReplacementTransform(n2Selected,n1Selected),
            Write(mid_xor_net[0][1]),
            Write(mid_xor_net[1][0])
        )

        self.play(ReplacementTransform(n2Selected,n1Selected))

        self.play(ReplacementTransform(holder,calculation[3]))

        self.play(ReplacementTransform(side_equations[0][1][1].copy(),equation))

        self.play(ReplacementTransform(a2.copy(),calculation[5][1]))
        self.play(ReplacementTransform(calculation[5][1].copy(),calculation[5][4]))

        self.play(ReplacementTransform(w2.copy(),calculation[2][1]))

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

        self.wait(10) # After this, everything is repeated

        self.play(Uncreate(calculation[1:6]))
        self.wait()
        self.play(Uncreate(equation))

        # Sets hidden bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        errorEqSelected = retainTransform(self,errorEqSelected,bEqSelected)

        holder = calculation[0]

        b1e_scaled = b1e.copy()
        b1e_scaled.scale(1/store_scale)

        calculation = VGroup(b1e_scaled,TexMobject("="),hidden_cz_derivative.copy())
        calculation.scale(0.4)
        calculation.arrange(buff=0.5)
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])

        self.play(ReplacementTransform(holder,calculation[2]))

        old_question_center = equation.get_center()
        equation = TexMobject(r"\frac{\partial C}{\partial b^l}", "=", r"\delta^l")
        equation.move_to(old_question_center)

        # Horizontally aligns equation components to calculation components
        align_horizontally(calculation,equation)

        self.play(ReplacementTransform(side_equations[0][2][1].copy(),equation))
        self.wait()
        self.play(Write(calculation[0:2]))

        self.play(ReplacementTransform(calculation[0].copy(),b1e))

        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(equation)
        )

        # Sets hidden weight error
        # ----------------------------------------------------------

        # Sets equation hightlight
        bEqSelected = retainTransform(self,bEqSelected,wEqSelected)
        
        w1e_scaled = w1e.copy()
        w1e_scaled.scale(1/store_scale)

        a1_scaled = a1.copy()
        a1_scaled.scale(1/store_scale)

        holder = calculation[2]
        calculation = VGroup(
            w1e_scaled,
            TexMobject("="),
            hidden_cz_derivative.copy(),
            VGroup(TexMobject(r"\Bigg("),a1_scaled,TexMobject(r"\Bigg)^T"))
        )
        calculation.scale(0.4)
        calculation[3].arrange(buff=0.1)
        calculation.arrange(buff=0.5)
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])
        self.play(ReplacementTransform(holder,calculation[2]))

        old_question_center = equation.get_center()
        equation = TexMobject(r"\frac{\partial C}{\partial w^l}" ,"=", r"\delta_l", r"(a^{l-1})^T")
        equation.move_to(old_question_center)

        align_horizontally(calculation,equation)

        self.play(ReplacementTransform(side_equations[0][3][1].copy(),equation))

        self.play(ReplacementTransform(a1.copy(),calculation[3][1]))

        self.play(
            Write(calculation[0:2]),
            Write(calculation[3][0]),
            Write(calculation[3][2])
        )

        self.play(ReplacementTransform(calculation[0].copy(),w1e))
        
        self.play(
            Uncreate(calculation[0:4]),
            Uncreate(equation[0:4])
        )

        self.wait(1) # Big pause before big explanation and end
        
        minus = TexMobject("-")
        minus.scale(0.5)

        calculation = VGroup(
            VGroup(w1.copy(),minus.copy(),w1e.copy()),
            VGroup(b1.copy(),minus.copy(),b1e.copy()),
            VGroup(w2.copy(),minus.copy(),w2e.copy()),
            VGroup(b2.copy(),minus.copy(),b2e.copy())
        )

        calculation[0].arrange(buff=0.1)
        calculation[1].arrange(buff=0.1)
        calculation[2].arrange(buff=0.1)
        calculation[3].arrange(buff=0.1)

        calculation.arrange(buff=0.5)

        calculation.move_to([side_equations_alignment + calculation.get_width()/2,current[0].get_y(),current[0].get_z()])

        self.play(
            Write(calculation[0][1]),
            Write(calculation[1][1]),
            Write(calculation[2][1]),
            Write(calculation[3][1]),
        )

        self.play(
            ReplacementTransform(w1.copy(),calculation[0][0]),
            ReplacementTransform(w1e.copy(),calculation[0][2]),

            ReplacementTransform(b1.copy(),calculation[1][0]),
            ReplacementTransform(b1e.copy(),calculation[1][2]),

            ReplacementTransform(w2.copy(),calculation[2][0]),
            ReplacementTransform(w2e.copy(),calculation[2][2]),

            ReplacementTransform(b2.copy(),calculation[3][0]),
            ReplacementTransform(b2e.copy(),calculation[3][2])
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
        self.play_backpropagation(title, side_equations)

# Transforms `a` -> `b`.
# Returns original value of `a`.
def retainTransform(scene,a,b):
    copy = a.copy()
    scene.play(ReplacementTransform(a,b))
    return copy

def rescale(obj,old,new):
    obj.scale(1/old)
    obj.scale(new)
    return obj

# Batch foreprop
class ep1_2(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.2,"Batch forepropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))

    def play_simd(self):
        v_buffer = 1.1

        simd_in = Matrix([1,2,3,4],v_buff=v_buffer)
        simd_ones = Matrix([1,1,1,1],v_buff=v_buffer)
        simd_out_pre = Matrix(["1+1","2+1","3+1","4+1"],v_buff=v_buffer)
        simd_out_post = Matrix([2,3,4,5],v_buff=v_buffer)
        simd = VGroup(simd_in,TexMobject("+"),simd_ones,TexMobject("="),simd_out_pre)
        simd.arrange()

        sisd_out_pre = VGroup(
            Matrix(["1+1"]),
            Matrix(["2+1"]),
            Matrix(["3+1"]),
            Matrix(["4+1"])
        )
        sisd_out_post = VGroup(
            Matrix([2]),
            Matrix([3]),
            Matrix([4]),
            Matrix([5])
        )
        sisd = VGroup(
            VGroup(Matrix([1]),TexMobject("+1="),sisd_out_pre[0]),
            VGroup(Matrix([2]),TexMobject("+1="),sisd_out_pre[1]),
            VGroup(Matrix([3]),TexMobject("+1="),sisd_out_pre[2]),
            VGroup(Matrix([4]),TexMobject("+1="),sisd_out_pre[3]),
        )
        for row in sisd:
            row.arrange()
        sisd.arrange(DOWN)
        
        simd_title = TextMobject("SIMD")
        simd_title.scale(1.5)
        sisd_title = TextMobject("SISD")
        sisd_title.scale(1.5)

        scene = VGroup(
            VGroup(simd_title,simd),
            VGroup(sisd_title,sisd)
        )
        title_distance = 1.2
        scene[0].arrange(DOWN,buff=title_distance)
        scene[1].arrange(DOWN,buff=title_distance)
        scene.arrange(buff=2)

        everything = VGroup(scene,simd_out_post,sisd_out_post)
        everything.scale(0.7)

        # Movement of unarranged things

        simd_out_post.move_to(simd_out_pre.get_center())
        for (post,pre) in zip(sisd_out_post,sisd_out_pre):
            post.move_to(pre.get_center())
        
        self.play(Write(scene))

        simd_box = Rectangle(color=YELLOW,height=simd.get_height()+0.3,width=simd.get_width()+0.3)
        sisd_box = Rectangle(color=YELLOW,height=sisd.get_height()+0.3,width=sisd.get_width()+0.3)
        # Moves highlight boxes to center on said thing they are highlighting
        simd_box.move_to(simd.get_center())
        sisd_box.move_to(sisd.get_center())

        self.play(Write(simd_box))

        self.play(ReplacementTransform(simd_out_pre[0],simd_out_post[0]))

        self.wait(2)

        self.play(ReplacementTransform(simd_box,sisd_box))

        self.play(ReplacementTransform(sisd_out_pre[0][0],sisd_out_post[0][0]))
        self.play(ReplacementTransform(sisd_out_pre[1][0],sisd_out_post[1][0]))
        self.play(ReplacementTransform(sisd_out_pre[2][0],sisd_out_post[2][0]))
        self.play(ReplacementTransform(sisd_out_pre[3][0],sisd_out_post[3][0]))

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

            Uncreate(sisd_box) # Uncreate highlight box
        )

        self.wait()

    def play_equations(self):
        side_equations = get_equations(equations=[
            r"a^{l+1} = A(z^l)",
            r"z^l = w^l a^l + b^l J_n"
        ],wheres=[r"J_n=[1_1,...,1_n]"],scale=0.4)
        
        title = TextMobject("Foreprop Equations")
        title.move_to(side_equations.get_center()+3*UP)

        self.play(Write(title))
        self.play(Write(side_equations))

        self.wait()

        self.play(Uncreate(title))

        return side_equations

    def play_batch_forwardpropagation(self,side_equations,store_scale=0.3,equation_scale=0.4):
        # Define some useful aliases
        # -----------------------------
        self.play(ReplacementTransform(side_equations,side_equations.copy().shift(5*LEFT)))
        side_equations_alignment = side_equations.get_x() + side_equations.get_width()/2 + 0.5

        # Sets up matricies with values
        a1 = Matrix([
            ["0","0","1","1"],
            ["0","1","0","1"]
        ],h_buff=1.2)
        a2 = Matrix([
            ["0.42...","0.47...","0.37...","0.42..."],
            ["0.57...","0.62...","0.59...","0.64..."],
            ["0.64...","0.52...","0.75...","0.64..."],
        ],h_buff=1.5)
        a3 = Matrix([
            ["0.53...","0.62...","0.65...","0.63..."],
            ["0.63...","0.53...","0.54...","0.54..."]
        ],h_buff=1.5)

        z1 = Matrix([
            ["-0.3","-0.1","-0.5","-0.3"],
            ["0.3","0.5","0.4","0.6"],
            ["0.6","0.1","1.1","0.6"]
        ],h_buff=1.2)
        z2 = Matrix([
            ["0.55...","0.49...","0.61...","0.56..."],
            ["0.15...","0.12...","0.18...","0.16..."]
        ],h_buff=1.5)

        w1 = Matrix([
            [-0.2,0.2],
            [0.1,0.2],
            [0.5,-0.5]
        ]).set_color(RED)
        w2 = Matrix([
            [-0.2,0.2,0.5],
            [0.1,0.2,0.3]
        ]).set_color(RED)

        b1 = Matrix([-0.3,0.3,0.6]).set_color(BLUE)
        b2 = Matrix([0.2,-0.2]).set_color(BLUE)
        bu = Matrix([[1,1,1,1]],h_buff=0.7)

        # Sets up matricies
        net_values_precise = VGroup(a1,w1,b1,z1,a2,w2,b2,z2,a3)
        net_values_precise.arrange()
        net_values_precise.scale(store_scale) # Scales up matricies
        # Shifts matricies up
        net_values_precise.shift(2*UP)

        # Gets small XOR net
        mid_xor_net = get_xor_net(0.5,0.25,2)
        # Shifts net down
        mid_xor_net.shift(2*DOWN)

        inputs = mid_xor_net[0][0]
        hidden = mid_xor_net[0][1]
        outputs = mid_xor_net[0][2]
        input_edges = mid_xor_net[1][0]
        output_edges = mid_xor_net[1][1]

        foreprop_header = TextMobject("Foreprogation")
        foreprop_header.shift(3*UP)

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
        a1_scaled = rescale(a1.copy(),store_scale,equation_scale) # ,h_buff=1.2
        a1_a1_scaled = a1_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        a1_a1_scaled.center()

        # Writes a1
        self.play(Write(a1_a1_scaled))
        # Stores a1
        self.play(ReplacementTransform(a1_a1_scaled.copy(),a1))
        # Uncreates a1
        self.play(Uncreate(a1_a1_scaled))

        self.wait()

        # ------------------------------------------------------------------------------------
        # z1
        # ------------------------------------------------------------------------------------

        # Highlights equation
        self.play(Write(eqZ))

        # Highlights matricies
        z1_highlight = get_highlight_box(VGroup(a1,w1,b1,z1))
        self.play(ReplacementTransform(a1_highlight,z1_highlight))

        # Highlights 1st hidden layer
        inputs.set_color(WHITE)
        input_edges.set_color(YELLOW)
        hidden.set_color(YELLOW)
        self.play(
            Write(input_edges), # Re-writes edges
            Write(hidden) # Re-writes to update
        )

        z1_scaled = rescale(z1.copy(),store_scale,equation_scale)
        z1_z1_scaled = z1_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        w1_scaled = rescale(w1.copy(),store_scale,equation_scale)

        b1_scaled = rescale(b1.copy(),store_scale,equation_scale)

        bu_scaled = bu.copy()
        bu_scaled.scale(equation_scale)
        z1_bu_scaled = bu_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        z1_a1_scaled = a1_scaled.copy()

        # z1 calculation
        z1_calculation = VGroup(
            z1_z1_scaled,
            TexMobject("="),
            w1_scaled,
            z1_a1_scaled,
            TexMobject("+"),
            b1_scaled,
            z1_bu_scaled
        )
        z1_calculation.arrange()

        # Aligns to side equations
        z1_calculation.move_to([
            side_equations_alignment + z1_calculation.get_width()/2,
            z1_calculation.get_y(),
            z1_calculation.get_z()
        ])

        # Pulls a1 into equation
        self.play(ReplacementTransform(a1.copy(),a1_scaled))
        # Pulls w1 into equation
        self.play(ReplacementTransform(w1.copy(),w1_scaled))
        # Pulls b1 into equation
        self.play(ReplacementTransform(b1.copy(),b1_scaled))
        
        # Writes operations
        self.play(
            Write(z1_z1_scaled),
            Write(z1_calculation[1]),
            Write(z1_calculation[4]),
            Write(z1_bu_scaled)
        )

        # Store z1
        self.play(ReplacementTransform(z1_z1_scaled.copy(),z1))

        self.wait(SCENE_WAIT)

        # Clears z1 calculation
        self.play(Uncreate(z1_calculation))

        # ------------------------------------------------------------------------------------
        # a2
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqZ = retainTransform(self,eqZ,eqA)

        # Highlights matricies
        a2_highlight = get_highlight_box(VGroup(z1,a2))
        self.play(ReplacementTransform(z1_highlight,a2_highlight))

        a2_scaled = rescale(a2.copy(),store_scale,equation_scale)
        a2_a2_scaled = a2_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        a2_z1_scaled = z1_scaled.copy()

        a2_calculation = VGroup(
            a2_a2_scaled,
            TexMobject("="),
            TexMobject(r"\sigma \Big("),
            a2_z1_scaled,
            TexMobject(r"\Big)")
        )
        a2_calculation.arrange()

        # Aligns to side equations
        a2_calculation.move_to([
            side_equations_alignment + a2_calculation.get_width()/2,
            a2_calculation.get_y(),
            a2_calculation.get_z()
        ])

        # Pulls z1 into equation
        self.play(ReplacementTransform(z1.copy(),a2_z1_scaled))

        # Writes operations
        self.play(
            Write(a2_a2_scaled),
            Write(a2_calculation[1:3]),
            Write(a2_calculation[4])
        )

        self.wait(SCENE_WAIT)

        # Store a2
        self.play(ReplacementTransform(a2_a2_scaled.copy(),a2))

        self.wait(SCENE_WAIT)

        # Clears equation
        self.play(Uncreate(a2_calculation))

        # ------------------------------------------------------------------------------------
        # z2
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqA = retainTransform(self,eqA,eqZ)

        # Highlights matricies
        z2_highlight = get_highlight_box(VGroup(a2,w2,b2,z2))
        self.play(ReplacementTransform(a2_highlight,z2_highlight))

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
            Write(outputs)
        )

        w2_scaled = rescale(w2.copy(),store_scale,equation_scale)

        z2_a2_scaled = a2_scaled.copy()

        b2_scaled = rescale(b2.copy(),store_scale,equation_scale)
        # Could scale this to match size of `input_weight_result`, but honestly who cares, this just adds unneccessary complexitity

        z2_scaled = rescale(z2.copy(),store_scale,equation_scale)
        z2_z2_scaled = z2_scaled.copy() # Re-used later, so we don't use and uncreate the base version

        z2_bu_scaled = bu_scaled.copy()

        z2_calculation = VGroup(
            z2_z2_scaled,
            TexMobject("="),
            w2_scaled,
            z2_a2_scaled,
            TexMobject("+"),
            b2_scaled,
            z2_bu_scaled
        )
        z2_calculation.arrange()

        # An admittedly kinda magic number scale, so it can fit on the screen
        z2_calculation.scale(0.8)

        # Aligns to side equations
        z2_calculation.move_to([
            side_equations_alignment + z2_calculation.get_width()/2,
            z2_calculation.get_y(),
            z2_calculation.get_z()
        ])

        # Pulls input weights into equation
        self.play(ReplacementTransform(a2.copy(),z2_a2_scaled))
        # Pulls input weights into equation
        self.play(ReplacementTransform(w2.copy(),w2_scaled))
        # Pulls biases into equation
        self.play(ReplacementTransform(b2.copy(),b2_scaled))
        # Writes operations
        self.play(
            Write(z2_z2_scaled),
            Write(z2_calculation[1]),
            Write(z2_calculation[4]),
            Write(z2_bu_scaled)
        )
        # Store result into matricies
        self.play(ReplacementTransform(z2_z2_scaled.copy(),z2))
        # Clears equation
        self.play(Uncreate(z2_calculation))

        # ------------------------------------------------------------------------------------
        # a3
        # ------------------------------------------------------------------------------------

        # Highlights equation
        eqZ = retainTransform(self,eqZ,eqA)

        a3_highlight = get_highlight_box(VGroup(z2,a3))
        self.play(ReplacementTransform(z2_highlight,a3_highlight))

        a3_scaled = rescale(a3.copy(),store_scale,equation_scale)

        a3_z2_scaled = z2_scaled.copy()

        a3_calculation = VGroup(
            a3_scaled,
            TexMobject("="),
            TexMobject(r"\sigma \Big("),
            a3_z2_scaled,
            TexMobject(r"\Big)")
        )
        a3_calculation.arrange()

        # Aligns to side equations
        a3_calculation.move_to([
            side_equations_alignment + a3_calculation.get_width()/2,
            a3_calculation.get_y(),
            a3_calculation.get_z()
        ])

        self.play(ReplacementTransform(z2.copy(),a3_z2_scaled))
        
        self.play(
            Write(a3_scaled),
            Write(a3_calculation[1:3]),
            Write(a3_calculation[4]),
        )

        # Stores a3
        self.play(ReplacementTransform(a3_scaled.copy(),a3))

        self.wait(SCENE_WAIT)

        self.play(Uncreate(a3_calculation))

        # Done
        # ------------------------------------------------------------------------------------

        self.play(Write(TextMobject("Contratz.")))

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

# Batch backprop
class ep1_3(Scene):
    def play_intro(self):
        title_scene = get_title_screen(1.3,"Batch backpropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))
    
    def play_equations(self):
        side_equations = get_equations(equations=[
            r"\delta^L = \nabla_a C \odot A'(z^L)",
            r"\delta^l = (w^{l+1})^T \delta^{l+1} \odot A'(z^l)",
            r"\frac{\partial C}{\partial b^l} = \delta^l J_n",
            r"\frac{\partial C}{\partial w^l} = \delta^l (a^l)^T"
        ], wheres=[r"\delta^l = \frac{\partial C}{\partial z^l}",r"J_n=[1_1,...,1_n]^T"])

        title = TextMobject("Batch backpropagation")
        title.move_to(side_equations.get_center()+3*UP)

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
        equation_buffer = 0.1
    ):

        # Sets up matricies with values
        # ----------------------------------------------------------
        a1 = Matrix([
            ["0","0","1","1"],
            ["0","1","0","1"]
        ],h_buff=0.6)
        a2 = Matrix([
            ["0.42...","0.47...","0.37...","0.42..."],
            ["0.57...","0.62...","0.59...","0.64..."],
            ["0.64...","0.52...","0.75...","0.64..."],
        ],h_buff=1.5)
        a3 = Matrix([
            ["0.53...","0.62...","0.65...","0.63..."],
            ["0.63...","0.53...","0.54...","0.54..."]
        ],h_buff=1.5)

        z1 = Matrix([
            ["-0.3","-0.1","-0.5","-0.3"],
            ["0.3","0.5","0.4","0.6"],
            ["0.6","0.1","1.1","0.6"]
        ],h_buff=1.2)
        z1e = Matrix([
            ["-0.00...","-0.01...","0.00...","0.00..."],
            ["0.01...","0.00...","0.02...","-0.00..."],
            ["0.02...","0.00...","0.00...","-0.01..."]
        ],h_buff=2)
        z2 = Matrix([
            ["0.55...","0.49...","0.61...","0.56..."],
            ["0.15...","0.12...","0.18...","0.16..."]
        ],h_buff=1.5)
        z2e = Matrix([
            ["0.12...","0.14...","-0.07...","-0.08..."],
            ["0.15...","-0.11...","0.13...","-0.1..."],
        ],h_buff=2)

        w1 = Matrix([
            [-0.2,0.2],
            [0.1,0.2],
            [0.5,-0.5]
        ]).set_color(RED)
        w1e = Matrix([
            ["0.00...","-0.00..."],
            ["0.01...","-0.00..."],
            ["-0.01...","-0.00..."]
        ],h_buff=2).set_color(GREEN)
        w2 = Matrix([
            [-0.2,0.2,0.5],
            [0.1,0.2,0.3]
        ],h_buff=1).set_color(RED)
        w2e = Matrix([
            ["0.05...","0.06...","0.43..."],
            ["0.12...","0.18...","0.23..."]
        ],h_buff=1.5).set_color(GREEN)

        b1 = Matrix([-0.3,0.3,0.6]).set_color(BLUE)
        b1e = Matrix(["-0.00...","0.03...","0.01..."]).set_color(GREEN)
        b2 = Matrix([0.2,-0.2]).set_color(BLUE)
        b2e = Matrix(["0.10...","0.15..."]).set_color(GREEN)

        bu = Matrix([1,1,1,1],h_buff=0.7)
        bu.scale(equation_scale)

        # Groups layer matricies
        n1 = VGroup(w1e,z1,b1,b1e,a2)
        n2 = VGroup(w2e,z2,b2,b2e,a3)

        # Sets side equation alignment
        new_side_equations = side_equations.copy()
        new_side_equations.scale(side_equation_scale)
        self.play(ReplacementTransform(side_equations,new_side_equations.copy().shift(5*LEFT).shift(0.3*DOWN)))
        side_equations_alignment = side_equations.get_x() + side_equations.get_width()/2 + side_equation_space

        # Scales all matricies
        net_values_precise = VGroup(a1,w1,w1e,z1,b1,b1e,a2,w2,w2e,z2,b2,b2e,a3)
        net_values_precise.arrange(buff=0.3)
        net_values_precise.scale(store_scale) # Scales down matricies
        net_values_precise.shift(2*UP)

        # Shifts so it is visible
        net_values_precise.shift(4*LEFT)

        # Sets highlight boxes
        # -----------------------------
        
        # Sets matrix highlight boxes
        n1Selected = get_highlight_box(n1,buffer=0.2)
        n2Selected = get_highlight_box(n2,buffer=0.2)

        # Sets equation highlight boxes
        outErrorEqSelected = get_highlight_box(side_equations[0][0])
        errorEqSelected = get_highlight_box(side_equations[0][1])
        bEqSelected = get_highlight_box(side_equations[0][2])
        wEqSelected = get_highlight_box(side_equations[0][3])

        # Sets net
        # -----------------------------

        mid_xor_net = get_xor_net(0.5,0.25,2)
        mid_xor_net.shift(2*DOWN)

        # Sets output scene
        # ----------------------------------------------------------
        
        a3_scaled = a3.copy()
        a3_scaled.scale(1/store_scale)
        a3_scaled.scale(equation_scale)
        a3_scaled.center()

        net_values_precise_excluding_errors = VGroup(a1,w1,w1e[1:3],z1,b1,b1e[1:3],a2,w2,w2e[1:3],z2,b2,b2e[1:3],a3)

        self.play(ReplacementTransform(title,title.copy().shift(0.5*UP)))
        self.play(
            Write(net_values_precise_excluding_errors),
            Write(a3_scaled),
            Write(mid_xor_net)
        )
        self.wait(10)

        # Sets output error
        # ----------------------------------------------------------

        target = Matrix([
            ["0","0","1","1"],
            ["0","1","0","1"]
        ],h_buff=1)
        target.scale(equation_scale)

        z2e.scale(equation_scale)

        z2_scaled = z2.copy()
        z2_scaled.scale(1/store_scale)
        z2_scaled.scale(equation_scale)

        # Sets calculation
        calculation = VGroup(
            z2e.copy(),
            TexMobject("="),
            VGroup(a3_scaled.copy(),TexMobject("-"),target),
            TexMobject(r"\odot"),
            VGroup(TexMobject(r"\sigma ' ("),z2_scaled.copy(),TexMobject(r")"))
        )
        calculation[2].arrange(buff=equation_buffer)
        calculation[4].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])

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
            Write(mid_xor_net[1][1])
        )

        self.play(ReplacementTransform(a3_scaled,calculation[2][0]))
        self.play(ReplacementTransform(z2.copy(),calculation[4][1]))

        # Writes calculation, avoiding rewriting transformed in matricies
        self.play(
            Write(calculation[0:2]),
            Write(calculation[2][1]),
            Write(calculation[2][2]),
            Write(calculation[3]),
            Write(calculation[4][0]),
            Write(calculation[4][2])
        )
        self.wait()

        self.play(Uncreate(calculation[1:5]))

        # Sets output bias error
        # ----------------------------------------------------------
        
        # Sets equation hightlight
        outErrorEqSelected = retainTransform(self,outErrorEqSelected,bEqSelected)

        holder = calculation[0] # Error holder

        b2e_scaled = b2e.copy()
        b2e_scaled.scale(1/store_scale)
        b2e_scaled.scale(equation_scale)

        # Sets calculation
        calculation = VGroup(b2e_scaled,TexMobject("="),z2e.copy(),bu.copy())
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])

        # Tranforms error into equation
        self.play(ReplacementTransform(holder,calculation[2]))

        self.wait()
        self.play(Write(calculation[0:2]),Write(calculation[3]))

        # Transforms result to bias error
        self.play(ReplacementTransform(calculation[0].copy(),b2e))

        # Uncreate calculation, sans error
        self.play(Uncreate(calculation[0:2]),Uncreate(calculation[3]))

        # Sets output weight error
        # ----------------------------------------------------------
        
        # Sets equation hightlight
        bEqSelected = retainTransform(self,bEqSelected,wEqSelected)

        w2e_scaled = w2e.copy()
        w2e_scaled.scale(1/store_scale)
        w2e_scaled.scale(equation_scale)

        a2_scaled = a2.copy()
        a2_scaled.scale(1/store_scale)
        a2_scaled.scale(equation_scale)

        holder = calculation[2]
        calculation = VGroup(
            w2e_scaled,
            TexMobject("="),
            z2e.copy(),
            VGroup(TexMobject(r"("),a2_scaled,TexMobject(r")^T"))
        )
        calculation[3].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)
        
        # Aligns calculation to side equations
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])
        
        # Tranforms error into calculation
        self.play(ReplacementTransform(holder,calculation[2]))

        # Transforms activations into calculation
        self.play(ReplacementTransform(a2.copy(),calculation[3][1]))

        # Writes calculation
        self.play(
            Write(calculation[0:2]),
            Write(calculation[3][0]),
            Write(calculation[3][2])
        )

        # Transforms result to weight error
        self.play(ReplacementTransform(calculation[0].copy(),w2e))
        
        # Uncreate equation, sans error
        self.play(
            Uncreate(calculation[0:2]),
            Uncreate(calculation[3])
        )
        self.wait()

        # Sets hidden neuron error
        # ----------------------------------------------------------

        # Sets equation hightlight
        wEqSelected = retainTransform(self,wEqSelected,errorEqSelected)

        z1e.scale(equation_scale)

        w2_scaled = w2.copy()
        w2_scaled.scale(1/store_scale)
        w2_scaled.scale(equation_scale)

        z1_scaled = z1.copy()
        z1_scaled.scale(1/store_scale)
        z1_scaled.scale(equation_scale)

        holder = calculation[2] # delta_l-1

        # Sets calculation
        calculation = VGroup(
            z1e.copy(),
            TexMobject("="),
            VGroup(TexMobject(r"("),w2_scaled,TexMobject(r")^T")),
            z2e.copy(),
            TexMobject(r"\odot"),
            VGroup(TexMobject(r"\sigma ' ("),z1_scaled.copy(),TexMobject(r")"))
        )
        calculation[2].arrange(buff=equation_buffer)
        calculation[5].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calcualtion to side equations
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])

        # Shifts highlight box to match matricies shift
        
        n1Selected.shift(8*RIGHT)

        values_sans_input_errors = VGroup(a1,w1,w1e[1:3],z1,b1,b1e[1:3],a2,w2,w2e,z2,b2,b2e,a3)
        
        w1e[0].shift(8*RIGHT)
        b1e[0].shift(8*RIGHT)
        
        shifted_values_sans_input_errors = values_sans_input_errors.copy()
        shifted_values_sans_input_errors.shift(8*RIGHT)

        mid_xor_net[0][2][0][0].set_color(WHITE)
        mid_xor_net[0][2][1][0].set_color(WHITE)
        mid_xor_net[1][1].set_color(WHITE)
        # Highlights output
        mid_xor_net[0][1].set_color(YELLOW)
        mid_xor_net[1][0].set_color(YELLOW)
        self.play(
            ReplacementTransform(n2Selected,n1Selected),
            ReplacementTransform(values_sans_input_errors,shifted_values_sans_input_errors), # Shifts so it is visible
            Write(mid_xor_net[0][1]),
            Write(mid_xor_net[1][0])
        )

        # Shifts matricies highlight box
        self.play(ReplacementTransform(n2Selected,n1Selected))

        # Pulls transforms matricies into calculation
        self.play(ReplacementTransform(holder,calculation[3]))
        self.play(ReplacementTransform(z1.copy(),calculation[5][1]))
        self.play(ReplacementTransform(w2.copy(),calculation[2][1]))

        # Write calculation, avoiding re-writing transformed in matricies
        self.play(
            Write(calculation[0:2]),
            Write(calculation[2][0]),
            Write(calculation[2][2]),
            Write(calculation[4]),
            Write(calculation[5][0]),
            Write(calculation[5][2]),
        )
        self.wait(10) # After this, everything is repeated

        # Uncreate calculation, sans error
        self.play(Uncreate(calculation[1:6]))
        self.wait()

        # Sets hidden bias error
        # ----------------------------------------------------------

        # Sets equation hightlight
        errorEqSelected = retainTransform(self,errorEqSelected,bEqSelected)

        holder = calculation[0]

        b1e_scaled = b1e.copy()
        b1e_scaled.scale(1/store_scale)
        b1e_scaled.scale(equation_scale)

        calculation = VGroup(b1e_scaled,TexMobject("="),z1e.copy(),bu.copy())
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])

        self.play(ReplacementTransform(holder,calculation[2]))

        # Writes calculation
        self.play(Write(calculation[0:2]),Write(calculation[3]))

        # Transforms result to bias error
        self.play(ReplacementTransform(calculation[0].copy(),b1e))

        # Uncreate calculation, sans error
        self.play(Uncreate(calculation[0:2]),Uncreate(calculation[3]))

        # Sets hidden weight error
        # ----------------------------------------------------------
        
        # Sets equation hightlight
        bEqSelected = retainTransform(self,bEqSelected,wEqSelected)

        w1e_scaled = w1e.copy()
        w1e_scaled.scale(1/store_scale)
        w1e_scaled.scale(equation_scale)

        a1_scaled = a1.copy()
        a1_scaled.scale(1/store_scale)
        a1_scaled.scale(equation_scale)

        holder = calculation[2]
        calculation = VGroup(
            w1e_scaled,
            TexMobject("="),
            z1e.copy(),
            VGroup(TexMobject(r"("),a1_scaled,TexMobject(r")^T"))
        )
        calculation[3].arrange(buff=equation_buffer)
        calculation.arrange(buff=equation_buffer)

        # Aligns calculation to side equations
        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])
        
        self.play(ReplacementTransform(holder,calculation[2]))

        # Transform matrix into calculation
        self.play(ReplacementTransform(a1.copy(),calculation[3][1]))

        # Writes calculation
        self.play(
            Write(calculation[0:2]),
            Write(calculation[3][0]),
            Write(calculation[3][2])
        )

        # Transforms result to weight error
        self.play(ReplacementTransform(calculation[0].copy(),w1e))
        
        # Uncreates calculation
        self.play(Uncreate(calculation))

        self.wait(1) # Big pause before big explanation and end
        
        minus = TexMobject("-")
        minus.scale(0.5)

        calculation = VGroup(
            VGroup(w1.copy(),minus.copy(),w1e.copy()),
            VGroup(b1.copy(),minus.copy(),b1e.copy()),
            VGroup(w2.copy(),minus.copy(),w2e.copy()),
            VGroup(b2.copy(),minus.copy(),b2e.copy())
        )

        calculation[0].arrange(buff=0.1)
        calculation[1].arrange(buff=0.1)
        calculation[2].arrange(buff=0.1)
        calculation[3].arrange(buff=0.1)

        calculation.arrange(buff=0.4)

        calculation.move_to([side_equations_alignment + calculation.get_width()/2,calculation.get_y(),calculation.get_z()])

        self.play(
            Write(calculation[0][1]),
            Write(calculation[1][1]),
            Write(calculation[2][1]),
            Write(calculation[3][1]),
        )

        self.play(
            ReplacementTransform(w1.copy(),calculation[0][0]),
            ReplacementTransform(w1e.copy(),calculation[0][2]),

            ReplacementTransform(b1.copy(),calculation[1][0]),
            ReplacementTransform(b1e.copy(),calculation[1][2]),

            ReplacementTransform(w2.copy(),calculation[2][0]),
            ReplacementTransform(w2e.copy(),calculation[2][2]),

            ReplacementTransform(b2.copy(),calculation[3][0]),
            ReplacementTransform(b2e.copy(),calculation[3][2])
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

# NOT CURRENTLY USED
# Given some matricies, aligns them to look like layers of a 3d tensor.
def set_layers(layers,distance=0.1,gradient=0.9,scaling=1):
    scale = 1
    perspective_lines = []
    obaqueness = 1
    for i in range(len(layers)-1):
        layers[i+1].fade(1 - obaqueness)

        layers[i+1].scale(scale)

        layers[i+1].move_to(layers[i].get_center()+(distance*UP)+(distance*RIGHT))

        h2s, w2s = layers[i].get_height()/2, layers[i].get_width()/2
        h2e, w2e = layers[i+1].get_height()/2, layers[i+1].get_width()/2

        cs = layers[i].get_center()
        xs, ys, zs = cs[0], cs[1], cs[2]
        ce = layers[i+1].get_center()
        xe, ye, ze = ce[0], ce[1], ce[2]

        lines = VGroup(
            DashedLine([xs+w2s,ys+h2s,zs],[xe+w2e,ye+h2e,ze]),
            DashedLine([xs+w2s,ys-h2s,zs],[xe+w2e,ye-h2e,ze]),
            DashedLine([xs-w2s,ys+h2s,zs],[xe-w2e,ye+h2e,ze]),
            DashedLine([xs-w2s,ys-h2s,zs],[xe-w2e,ye-h2e,ze])
        )
        lines.fade(1 - obaqueness)

        perspective_lines.append(lines)

        scale *= scaling
        obaqueness *= gradient
        distance *= scaling

    return VGroup(*perspective_lines)

# TODO
# - Regularisation (L2 + dropout)
# - Initialisation
# - Different cost functions (quadratic + crossentropy)
# - Different activations (sigmoid + tanh + softmax + relu + lrelu)

# Convolution
class ep2_0(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.0,"Convolution")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))
    
    def play_conv(self,scale=0.5,label_spacing=0.5,arrow_spacing=0.02,image_size=(3,3),filter_size=(2,2)):
        title = TextMobject("Convolution")
        title.shift(3*UP)
        self.play(Write(title))

        componentwise_equation = TexMobject(r"out_{i,j} = (in * filter)_{i,j} = \sum_{m=1}^h \sum_{n=1}^w in_{i+m,j+n} filter_{m,n} + b")
        matrix_equation = TexMobject(r"out = (in * filter) = in \cdot filter^T + b J_{h,w}")
        equation = VGroup(componentwise_equation,matrix_equation)
        equation.arrange(DOWN)
        equation.scale(scale)

        image_vals = [[random.randint(0,2) for x in range(image_size[0])] for y in range(image_size[1])]
        image = Matrix(image_vals)
        image_vals = sum(image_vals,[])
        img_label = TextMobject("Image/Input")
        img_label.scale(scale)

        # Sets image axis labels
        filter_rows = TexMobject(r"h")
        filter_cols = TexMobject(r"w")
        filter_rows.scale(scale)
        filter_cols.scale(scale)
        
        filt_vals = [[random.randint(0,1) for x in range(filter_size[0])] for y in range(filter_size[1])]
        filt = Matrix(filt_vals)
        filt_vals = sum(filt_vals,[])
        filt_label = TextMobject("Filter/Kernel")
        filt_label.scale(scale)
        
        temp = Matrix([[0 for x in range(filter_size[0])] for y in range(filter_size[1])]).set_color(YELLOW)
        
        filt_group = VGroup(filt,TexMobject("\odot"),temp)
        filt_group.arrange(buff=0.5)

        feature_size = (image_size[0]-filter_size[0]+1,image_size[1]-filter_size[1]+1)
        feature = Matrix([
            [0 for x in range(feature_size[0])]
            for y in range(feature_size[1])
        ])
        feature_label = TextMobject("Feature/Output")
        feature_label.scale(scale)

        scene = VGroup(image,filt_group,feature)
        scene.arrange(buff=3)

        scene.scale(scale)
        
        calculation = VGroup(*[TexMobject("placeholder") for i in range(filter_size[1])])

        self.play(
            Write(image),
            Write(filt_group[0:2]),
            Write(temp[1:3]),
            Write(feature[1:3])
        )

        highlight = Rectangle(color=YELLOW,height=filt.get_height(),width=filt.get_width())#.set_fill(YELLOW, opacity=0.1)
        
        element_size = [filt.get_width()/filter_size[0],filt.get_height()/filter_size[1]]
        shift = [filt.get_width()/2-element_size[0]/2,-filt.get_height()/2+element_size[1]/2,0]

        img_label.move_to(image.get_center()+[0,image.get_height()/2+img_label.get_height()/2+label_spacing+element_size[1],0])
        filt_label.move_to(filt.get_center()+[0,filt.get_height()/2+filt_label.get_height()/2+label_spacing+element_size[1],0])
        feature_label.move_to(feature.get_center()+[0,feature.get_height()/2+feature_label.get_height()/2+label_spacing+element_size[1],0])
        
        filter_rows.move_to(filt.get_center()-[filt.get_width()/2+filter_rows.get_width()/2+label_spacing/4,0,0])
        filter_cols.move_to(filt.get_center()-[0,filt.get_height()/2+filter_cols.get_height()/2+label_spacing/4,0])

        equation.move_to(filt_group.get_center()-[0,filt_group.get_height()/2+equation.get_height()/2+label_spacing,0])

        self.play(
            Write(img_label),
            Write(filt_label),
            Write(feature_label),
            Write(filter_rows),
            Write(filter_cols),
            Write(equation)
        )

        written = []

        for yi in range(0,feature_size[1]):
            for xi in range(0,feature_size[0]):
                # Gets index in image
                image_indx = xi+yi*image_size[0]

                # Gets and sets values in local receptive field
                temp_vals = [[image_vals[(xi+x)+(yi+y)*image_size[0]] for x in range(filter_size[0])] for y in range(filter_size[1])]
                new_temp = Matrix(temp_vals).set_color(YELLOW)
                new_temp.scale(scale)
                new_temp.move_to(temp.get_center())

                # Gets result and calculation string
                multiplying = ["" for i in range(filter_size[1])]
                result = 0
                for indx,y in enumerate(range(filter_size[1])):
                    for x in range(filter_size[0]):
                        filter_value = filt_vals[x+y*filter_size[0]]
                        image_value = image_vals[(xi+x)+(yi+y)*image_size[0]]

                        multiplying[indx] += "("+str(filter_value)+"\\cdot"+str(image_value)+")"

                        result += filter_value*image_value

                        if (x == filter_size[0]-1 and y == filter_size[1]-1):
                            multiplying[indx] += " = " + str(result)
                        else:
                            multiplying[indx] += "+"
                        
                # Gets index in feature
                feature_indx = xi+yi*feature_size[0]

                if (xi==0 and yi==0):
                    # Sets highlight
                    highlight.move_to(image[0][image_indx].get_center()+shift)

                    # Sets calculation string
                    calculation = VGroup(*[TexMobject(line) for line in multiplying])
                    calculation.scale(scale)
                    calculation.arrange(DOWN,buff=0.2)
                    calculation.move_to(
                        equation.get_center()-
                        [0,equation.get_height()/2+calculation.get_height()/2+label_spacing,0]
                    )

                    # Sets arrow to feature
                    arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        feature[0][feature_indx].get_center()-[feature[0][feature_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    arrow.fade(0.5)

                    # Writes
                    self.play(
                        Write(highlight),
                        Transform(temp[0],new_temp[0]),
                        Write(calculation),
                        Write(arrow)
                    )
                else:
                    # Sets highlight
                    new_highlight = highlight.copy()
                    new_highlight.move_to(image[0][image_indx].get_center()+shift)

                    # Sets calculation string
                    new_calculation = VGroup(*[TexMobject(line) for line in multiplying])
                    new_calculation.scale(scale)
                    new_calculation.arrange(DOWN,buff=0.2)
                    new_calculation.move_to(calculation.get_center())

                    # Sets arrow to feature
                    new_arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        feature[0][feature_indx].get_center()-[feature[0][feature_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    new_arrow.fade(0.5)

                    # Writes
                    self.play(
                        Transform(highlight,new_highlight),
                        Transform(temp[0],new_temp[0]),
                        Transform(calculation,new_calculation),
                        Transform(arrow,new_arrow)
                    )

                # Sets and writes result
                resul_obj = TexMobject(str(result))
                resul_obj.scale(scale)
                resul_obj.move_to(feature[0][feature_indx].get_center())
                self.play(Write(resul_obj))
                written.append(resul_obj)

                self.wait()

        written = VGroup(*written)

        self.play(
            Uncreate(arrow),
            Uncreate(calculation),
            Uncreate(highlight)
        )

        return (image,feature,filt,temp,image_size,filter_size,image_vals,filt_vals,equation,written)

    def play_padding_conv(
        self,image,feature,filt,temp,image_size,filter_size,image_vals,
        filt_vals,equation,label_spacing=0.5,scale=0.5,arrow_spacing=0.02
    ):
        # Gets highlight
        highlight = Rectangle(color=YELLOW,height=filt.get_height(),width=filt.get_width())

        # Sets and writes subtitle
        subtitle = TextMobject("Zero padding")
        subtitle.scale(0.6)
        subtitle.shift(2.6*UP)
        self.play(Write(subtitle))

        # Sets new image size and buffer
        buffer = (int(filter_size[0]/2),int(filter_size[1]/2))
        padded_image_size = [image_size[0]+2*buffer[0],image_size[1]+2*buffer[1]]
        
        # Gets and sets zero-padded image
        padded_image_vals = []
        for y in range(0,padded_image_size[1]):
            holder = []
            for x in range(0,padded_image_size[0]):
                if (y<buffer[1] or x<buffer[0] or y>image_size[1] or x>image_size[0]):
                    holder.append(0)
                else:
                    holder.append(image_vals[(x-buffer[0])+(y-buffer[1])*image_size[0]])
            padded_image_vals.append(holder)
        padded_image = Matrix(padded_image_vals)
        padded_image.scale(scale)
        padded_image.move_to(image.get_center())

        # Sets group containg all the padding zeros
        padding = []
        for y in range(0,padded_image_size[1]):
            for x in range(0,padded_image_size[0]):
                if (y<buffer[1] or x<buffer[0] or y>image_size[1] or x>image_size[0]):
                    padding.append(padded_image[0][x+y*padded_image_size[0]])
        padding = VGroup(*padding)

        # Sets non padded image holder
        image_holder = image.copy()

        # Transforms brackets but retains copy of old brackets
        image_brackets = retainTransform(self,image[1:3],padded_image[1:3])
        
        # Writes zero padding
        self.play(Write(padding))

        # Flattens image values
        image_vals = sum(padded_image_vals,[])
        
        # Sets new feature
        feature_size = (padded_image_size[0]-filter_size[0]+1,padded_image_size[1]-filter_size[1]+1)
        padded_feature = Matrix([
            [0 for x in range(feature_size[0])] # `0` simply being used as placeholder value
            for y in range(feature_size[1])
        ])
        padded_feature.scale(scale)
        padded_feature.move_to(feature.get_center())

        # Transforms brackets but retains copy of old brackets
        feature_brackets = retainTransform(self,feature[1:3],padded_feature[1:3])

        # Sets element size and needed highlight shift
        element_size = [filt.get_width()/filter_size[0],filt.get_height()/filter_size[1]]
        shift = [filt.get_width()/2-element_size[0]/2,-filt.get_height()/2+element_size[1]/2,0]
        
        # Defines container for all newly written feature values
        written = []

        for yi in range(0,feature_size[1]):
            for xi in range(0,feature_size[0]):
                # Gets image index
                image_indx = xi+yi*padded_image_size[0]

                # Gets  and sets local receptive field values
                temp_vals = [[image_vals[(xi+x)+(yi+y)*padded_image_size[0]] for x in range(filter_size[0])] for y in range(filter_size[1])]
                new_temp = Matrix(temp_vals).set_color(YELLOW)
                new_temp.scale(scale)
                new_temp.move_to(temp.get_center())

                # Defines calculation string
                multiplying = ["" for i in range(filter_size[1])]
                result = 0

                for indx,y in enumerate(range(filter_size[1])):
                    for x in range(filter_size[0]):
                        filter_value = filt_vals[x+y*filter_size[0]]
                        image_value = image_vals[(xi+x)+(yi+y)*padded_image_size[0]]

                        multiplying[indx] += "("+str(filter_value)+"\\cdot"+str(image_value)+")"

                        result += filter_value*image_value

                        if (x == filter_size[0]-1 and y == filter_size[1]-1):
                            multiplying[indx] += " = " + str(result)
                        else:
                            multiplying[indx] += "+"
                        
                feature_indx = xi+yi*feature_size[0]

                if (xi==0 and yi==0):
                    # Sets highlight
                    highlight.move_to(padded_image[0][image_indx].get_center()+shift)

                    # Sets calculation
                    calculation = VGroup(*[TexMobject(line) for line in multiplying])
                    calculation.scale(scale)
                    calculation.arrange(DOWN,buff=0.2)
                    calculation.move_to(
                        equation.get_center()-
                        [0,equation.get_height()/2+calculation.get_height()/2+label_spacing,0]
                    )

                    # Sets arrow
                    arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        padded_feature[0][feature_indx].get_center()-[padded_feature[0][feature_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    arrow.fade(0.5)

                    # Writes
                    self.play(
                        Write(arrow),
                        Write(calculation),
                        Write(highlight),
                        Transform(temp[0],new_temp[0])
                    )
                else:
                    # Sets highlight
                    new_highlight = highlight.copy()
                    new_highlight.move_to(padded_image[0][image_indx].get_center()+shift)

                    # Sets calculation
                    new_calculation = VGroup(*[TexMobject(line) for line in multiplying])
                    new_calculation.scale(scale)
                    new_calculation.arrange(DOWN,buff=0.2)
                    new_calculation.move_to(calculation.get_center())
                    self.play()

                    # Sets arrow
                    new_arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        padded_feature[0][feature_indx].get_center()-[padded_feature[0][feature_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    new_arrow.fade(0.5)

                    # Writes
                    self.play(
                        Transform(arrow,new_arrow),
                        Transform(calculation,new_calculation),
                        Transform(highlight,new_highlight),
                        Transform(temp[0],new_temp[0])
                    )

                # Writes padding result
                if (yi==0 or xi==0 or xi==feature_size[0]-1 or yi==feature_size[1]-1):
                    resul_obj = TexMobject(str(result))
                    resul_obj.scale(scale)
                    resul_obj.move_to(padded_feature[0][feature_indx].get_center())
                    self.play(Write(resul_obj))
                    written.append(resul_obj)
                self.wait()

        # Uncreates
        self.play(Uncreate(subtitle))
        self.play(
            Uncreate(arrow),
            Uncreate(highlight),
            Uncreate(calculation)
        )
        self.play(
            Uncreate(padding),
            Uncreate(VGroup(*written))
        )
        self.play(
            ReplacementTransform(padded_image[1:3],image_brackets),
            ReplacementTransform(padded_feature[1:3],feature_brackets)
        )

        return image_holder
    
    def play_channels_conv(self,image,feature,filt,temp,image_vals,filt_vals,equation,written,image_size=(3,3),filter_size=(2,2),layers=3,label_spacing=0.5,scale=0.5,arrow_spacing=0.02):
        # Uncreates all feature values
        self.play(Uncreate(written))

        # Sets subtitle
        subtitle = TextMobject("Channels")
        subtitle.scale(0.6)
        subtitle.shift(2.6*UP)

        # Sets filter depth label
        filter_depth = TexMobject(r"d")
        filter_depth.scale(scale)
        filter_depth.move_to(
            filt.get_center()-
            [
                filt.get_width()/2+filter_depth.get_width()/2+label_spacing/4,
                filt.get_height()/2+filter_depth.get_height()/2+label_spacing/4,
                0
            ]
        )

        # Sets equation
        new_equation = TexMobject(r"out_{i,j} = (in * filters)_{i,j} = \sum_{l=1}^d \sum_{m=1}^h \sum_{n=1}^w in_{i+m,j+n,l} \cdot filter_{m,n,l} + b")
        new_equation.scale(scale)
        new_equation.move_to(equation.get_center())

        # Writes subtitle, depth label and equation
        self.play(
            Write(subtitle),
            Write(filter_depth),
            ReplacementTransform(equation,new_equation)
        )

        # Sets and writes new layers to image, filter and local receptive field
        images = VGroup(*[image.copy() for i in range(layers)])
        lines = set_layers(images)

        filters = VGroup(*[filt]+[filt.copy() for i in range(layers-1)])
        lines = set_layers(filters)

        temps = VGroup(*[temp]+[temp.copy() for i in range(layers-1)])
        lines = set_layers(temps)

        self.play(
            Write(images[1:layers]),
            Write(filters[1:layers]),
            Write(temps[1:layers])
        )

        
        # Sets feature size
        feature_size = (image_size[0]-filter_size[0]+1,image_size[1]-filter_size[1]+1)

        # Sets element size and highlight shift
        element_size = [filt.get_width()/filter_size[0],filt.get_height()/filter_size[1]]
        shift = [filt.get_width()/2-element_size[0]/2,-filt.get_height()/2+element_size[1]/2,0]

        # Sets highlight
        highlight = Rectangle(color=YELLOW,height=filt.get_height(),width=filt.get_width())

        for yi in range(0,feature_size[1]):
            for xi in range(0,feature_size[0]):
                # Sets image index
                image_indx = xi+yi*image_size[0]

                # Sets local receptive field
                temp_vals = [[image_vals[(xi+x)+(yi+y)*image_size[0]] for x in range(filter_size[0])] for y in range(filter_size[1])]
                new_temp = Matrix(temp_vals).set_color(YELLOW)
                new_temp.scale(scale)
                new_temp.move_to(temps[0].get_center())
                new_temps = VGroup(*[new_temp.copy() for i in range(layers)])
                lines = set_layers(new_temps)

                # Define calculation string
                multiplying = ["" for i in range(layers)]
                result = 0
                for z in range(layers):
                    multiplying[z] += "["
                    for y in range(filter_size[1]):
                        for x in range(filter_size[0]):
                            filter_value = filt_vals[x+y*filter_size[0]]
                            image_value = image_vals[(xi+x)+(yi+y)*image_size[0]]

                            multiplying[z] += "("+str(filter_value)+"\\cdot"+str(image_value)+")"

                            result += filter_value*image_value
                            if (x == filter_size[0]-1 and y == filter_size[1]-1):
                                multiplying[z] += "]"
                                if (z==layers-1):
                                    multiplying[z] += " = " + str(result)
                            else:
                                multiplying[z] += "+"
                    
                # Sets feature index
                feature_indx = xi+yi*feature_size[0]

                if (xi==0 and yi==0):
                    # Sets highlight
                    highlight.move_to(image[0][image_indx].get_center()+shift)
                    highlights = VGroup(*[highlight.copy() for i in range(layers)])
                    lines = set_layers(highlights)

                    # Sets calculation
                    calculation = VGroup(*[TexMobject(line) for line in multiplying])
                    calculation.scale(scale)
                    calculation.arrange(DOWN,buff=0.2)
                    calculation.move_to(
                        equation.get_center()-
                        [0,equation.get_height()/2+calculation.get_height()/2+label_spacing,0]
                    )

                    # Sets arrow
                    arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        feature[0][feature_indx].get_center()-[feature[0][feature_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    arrow.fade(0.5)

                    # Writes
                    self.play(
                        Write(highlights),
                        Transform(temps,new_temps),
                        Write(calculation),
                        Write(arrow)
                    )
                else:
                    # Sets highlight
                    distance = image[0][image_indx].get_center() - highlights[0].get_center()
                    new_highlights = highlights.copy()
                    new_highlights.shift(distance+shift)

                    # Sets calculation
                    new_calculation = VGroup(*[TexMobject(line) for line in multiplying])
                    new_calculation.scale(scale)
                    new_calculation.arrange(DOWN,buff=0.2)
                    new_calculation.move_to(calculation.get_center())

                    # Sets arrow
                    new_arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        feature[0][feature_indx].get_center()-[feature[0][feature_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    new_arrow.fade(0.5)

                    # Writes
                    self.play(
                        Transform(highlights,new_highlights),
                        Transform(temps,new_temps),
                        Transform(calculation,new_calculation),
                        Transform(arrow,new_arrow)
                    )
                # Writes feature value
                if (yi==0 or xi==0 or xi==feature_size[0]-1 or yi==feature_size[1]-1):
                    resul_obj = TexMobject(str(result))
                    resul_obj.scale(scale)
                    resul_obj.move_to(feature[0][feature_indx].get_center())
                    self.play(Write(resul_obj))
                self.wait()

    def construct(self):
        self.play_intro()

        image, feature, filt, temp, image_size, filter_size, image_vals, filt_vals, equation, written = self.play_conv()

        image = self.play_padding_conv(image, feature, filt, temp, image_size, filter_size, image_vals, filt_vals, equation)

        self.play_channels_conv(image,feature,filt,temp,image_vals,filt_vals,equation,written)

        self.wait(3)

# Pooling
class ep2_1(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.1,"Pooling")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))
    
    def max_pool(self,scale=0.5,label_spacing=0.5,arrow_spacing=0.02,image_size=(4,4),pool_size=(2,2)):
        title = TextMobject("Pooling")
        title.shift(3*UP)

        subtitle = TextMobject("Max pooling")
        subtitle.scale(0.6)
        subtitle.shift(2.6*UP)

        equation = TexMobject(r"\max(\{{in_{ih+m,jw+n} | n∪m⊆ℤ, 1 \leq m \leq h, 1 \leq n \leq w}\}) = out_{i+1,j+1}")
        equation.scale(scale)

        self.play(
            Write(title),
            Write(subtitle)
        )

        image_vals = [[random.randint(0,5) for x in range(image_size[0])] for y in range(image_size[1])]
        image = Matrix(image_vals)
        image_vals = sum(image_vals,[])

        img_label = TextMobject("Image/Input")
        img_label.scale(scale)
        
        temp = Matrix([[image_vals[x+y*image_size[0]] for x in range(pool_size[0])] for y in range(pool_size[1])]).set_color(YELLOW)

        new_image_size = (int(image_size[0]/pool_size[0]),int(image_size[1]/pool_size[1]))
        new_image = Matrix([
            [0 for x in range(new_image_size[0])]
            for y in range(new_image_size[1])
        ])
        new_image_label = TextMobject("New image/Output")
        new_image_label.scale(scale)

        scene = VGroup(image,temp,new_image)
        scene.arrange(buff=3)
        scene.scale(scale)

        self.play(
            Write(image),
            Write(temp[1:3]),
            Write(new_image[1:3]),
        )
        
        # Sets image axis labels
        pool_rows = TexMobject(r"h")
        pool_cols = TexMobject(r"w")
        pool_rows.scale(scale)
        pool_cols.scale(scale)

        element_size = (image.get_width()/image_size[0],image.get_height()/image_size[1])
        shift = (temp.get_width()/2-element_size[0]/2,-temp.get_height()/2+element_size[1]/2,0)

        img_label.move_to(image.get_center()+[0,image.get_height()/2+img_label.get_height()/2+label_spacing,0])
        new_image_label.move_to(new_image.get_center()+[0,new_image.get_height()/2+new_image_label.get_height()/2+label_spacing,0])

        pool_rows.move_to(temp.get_center()-[temp.get_width()/2+pool_rows.get_width()/2+label_spacing/4,0,0])
        pool_cols.move_to(temp.get_center()-[0,temp.get_height()/2+pool_cols.get_height()/2+label_spacing/4,0])

        equation.move_to(temp.get_center()-[0,temp.get_height()/2+equation.get_height()/2+2*label_spacing,0])

        self.play(
            Write(img_label),
            Write(new_image_label),

            Write(pool_rows),
            Write(pool_cols),

            Write(equation)
        )

        highlight = Rectangle(color=YELLOW,height=temp.get_height(),width=temp.get_width())#.set_fill(YELLOW, opacity=0.1)

        calculation = TexMobject("placeholder")

        for yi,yni in zip(range(0,image_size[1],pool_size[1]),range(0,new_image_size[1])):
            for xi,xni in zip(range(0,image_size[0],pool_size[0]),range(0,new_image_size[0])):
                # Sets image index
                img_indx = xi+yi*image_size[0]

                # Sets calculation string
                max_of = "max("
                max_val = -1
                for y in range(pool_size[1]):
                    for x in range(pool_size[0]):
                        image_value = image_vals[(xi+x)+(yi+y)*image_size[0]]
                        max_of += str(image_value)
                        max_val = max(max_val,image_value)
                        if not (x == pool_size[0]-1 and y == pool_size[1]-1):
                            max_of += ","
                max_of += ")="+str(max_val)
                        
                # Sets pooled image index
                pooled_img_indx = xni+yni*new_image_size[0]

                if (xi==0 and yi==0):
                    # Sets highlight
                    highlight.move_to(image[0][img_indx].get_center()+shift)

                    # Sets calculation string
                    calculation = TexMobject(max_of)
                    calculation.scale(scale)
                    calculation.move_to(
                        equation.get_center()-
                        [0,equation.get_height()/2+calculation.get_height()/2+label_spacing,0]
                    )

                    # Sets arrow
                    arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        new_image[0][pooled_img_indx].get_center()-[new_image[0][pooled_img_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    arrow.fade(0.5)

                    # Writes
                    self.play(
                        Write(highlight),
                        Write(temp[0]),
                        Write(calculation),
                        Write(arrow)
                    )
                else:
                    # Sets highlight
                    new_highlight = highlight.copy()
                    new_highlight.move_to(image[0][img_indx].get_center()+shift)

                    # Sets receptive field
                    temp_vals = [[image_vals[(xi+x)+(yi+y)*image_size[0]] for x in range(pool_size[0])] for y in range(pool_size[1])]
                    new_temp = Matrix(temp_vals).set_color(YELLOW)
                    new_temp.scale(scale)
                    new_temp.move_to(temp.get_center())

                    # Sets calculation string
                    new_calculation = TexMobject(max_of)
                    new_calculation.scale(scale)
                    new_calculation.move_to(calculation.get_center())

                    # Sets arrow
                    new_arrow = Arrow(
                        temp.get_center()+[temp.get_width()/2+arrow_spacing,0,0],
                        new_image[0][pooled_img_indx].get_center()-[new_image[0][pooled_img_indx].get_width()/2+arrow_spacing,0,0],
                    stroke_width=5,max_tip_length_to_length_ratio=0.07)
                    new_arrow.fade(0.5)
                    
                    # Writes
                    self.play(
                        Transform(highlight,new_highlight),
                        Transform(temp[0],new_temp[0]),
                        Transform(calculation,new_calculation),
                        Transform(arrow,new_arrow)
                    )

                
                resul_obj = TexMobject(str(max_val))
                resul_obj.scale(scale)
                resul_obj.move_to(new_image[0][pooled_img_indx].get_center())
                self.play(Write(resul_obj))

                self.wait()

    def construct(self):
        self.play_intro()

        self.max_pool()

        self.wait(3)

def get_matrix_conv_net(
    conv_layers,
    dense_layers,
    input_scale=0.4,
    filter_scale=0.7,
    arrow_spacing=0.1,
    layer_spacing=2,
    neuron_spacing=0.2,
    neuron_radius=0.1,
    in_shape = (0,0),
):
    # Adds input#
    inputs = VGroup(*[TexMobject("placeholder")])
    if in_shape == (0,0):
        inputs = VGroup(Matrix([
                ["a_{1,1,1}","\\dots","a_{1,1,n_1}"],
                ["\\vdots","\\ddots","\\vdots"],
                ["a_{1,m_1,1}","\\dots","a_{1,m_1,n_1}"],
        ],h_buff=1.8,v_buff=1.8))
        
    else:
        inputs = VGroup(Matrix([["a_{"+str(x+1)+","+str(y+1)+"}" for x in range(in_shape[1])] for y in range(in_shape[0])]))

    inputs.scale(input_scale)

    filt = Matrix(["\\ddots"])
    filt.scale(filter_scale)

    # Adds conv layers
    layers = [
        VGroup(*[filt.copy() for c in range(layer)])
        for layer in conv_layers
    ]
    for layer in layers:
        set_layers(layer)
    layers.insert(0,inputs)
    for i in range(1,len(layers)):
        layers[i].shift([layers[i-1][0].get_x()+layers[i-1][0].get_width()/2+layers[i][0].get_width()/2+layer_spacing,0,0])

    # Adds dense layers
    connections = []
    for i in range(len(dense_layers)):
        dense = VGroup(*[Circle(radius=neuron_radius,stroke_color=WHITE,stroke_width=1) for j in range(dense_layers[i])])
        dense.arrange(DOWN,buff=neuron_spacing)

        if i==0:
            dense.shift([layers[-1][0].get_x()+layers[-1][0].get_width()/2+dense.get_width()/2+layer_spacing,0,0])
        else:
            dense.shift([layers[-1].get_x()+layers[-1].get_width()/2+dense.get_width()/2+layer_spacing/2,0,0])

        layers.append(dense)
        # Not first dense layer
        if i != 0:
            layer_connections = VGroup(*[
                Line(
                    layers[-2][j].get_center()+[layers[-2][j].get_width()/2,0,0],
                    layers[-1][k].get_center()-[layers[-1][k].get_width()/2,0,0],
                    stroke_width=2
                ) 
                for j in range(len(layers[-2])) for k in range(len(layers[-1])) 
            ])
            connections.append(layer_connections)

    # Adds arrows between conv layers and first dense layer
    arrows = [
        Arrow(
            layers[i][0].get_center()+[layers[i][0].get_width()/2+arrow_spacing,0,0],
            layers[i+1][0].get_center()-[layers[i+1][0].get_width()/2+arrow_spacing,0,0]
        )
        for i in range(0,len(conv_layers))
    ]
    l_conv= len(conv_layers)
    arrows.append(Arrow(
            layers[l_conv][0].get_center()+[layers[l_conv][0].get_width()/2+arrow_spacing,0,0],
            layers[l_conv+1].get_center()-[layers[l_conv+1].get_width()/2+arrow_spacing,0,0]
    ))

    net = VGroup(VGroup(*layers),VGroup(*arrows),VGroup(*connections))
    net.center()
    return net

def get_explicit_conv_net(
    in_shape, # (y,x)/(m,n)
    conv_layers,
    dense_layers,
    scale=0.4,
    arrow_spacing=0.05,
    layer_spacing=1,
    circle_spacing=0.2
):
    # Adds input
    inputs = VGroup(Matrix([str(in_shape[1])+"\\times"+str(in_shape[0])]))
    inputs.scale(scale)

    # Adds conv layers
    layers = [inputs]
    layers += [
        Matrix([str(i)+"\\times"+"("+str(m)+"\\times"+str(n)+")"]).scale(scale)
        for (i,m,n) in conv_layers
    ]
    circles = []
    for layer in dense_layers:
        num = TextMobject(str(layer)).scale(scale)
        layers += num

    layers = VGroup(*layers)
    layers.arrange(buff=layer_spacing)

    circles = []
    for indx in range(len(dense_layers)):
        circ = Circle(radius=layers[indx+len(conv_layers)+1].get_height()/2+circle_spacing,color=WHITE,stroke_width=2)
        circ.move_to(layers[indx+len(conv_layers)+1].get_center())
        circles += circ

    # Adds arrows between layers
    arrows = [
        Arrow(
            layers[i].get_center()+[layers[i].get_width()/2+arrow_spacing,0,0],
            layers[i+1].get_center()-[layers[i+1].get_width()/2+arrow_spacing,0,0]
        )
        for i in range(len(layers)-1)
    ]

    net = VGroup(layers,VGroup(*arrows),VGroup(*circles))
    net.center()
    return net

def get_denseish_conv_net(
    conv_layers,
    dense_layers,
    input_scale=0.3,
    filter_scale=0.2,
    filter_spacing=0.1,
    neuron_spacing=0.1,
    neuron_radius=0.05,
    layer_spacing=1
):
        inputs = VGroup(Matrix([
            ["a_{1,1,1}","\\dots","a_{1,1,n_1}"],
            ["\\vdots","\\ddots","\\vdots"],
            ["a_{1,m_1,1}","\\dots","a_{1,m_1,n_1}"],
        ],h_buff=1.8,v_buff=1.8))
        inputs.scale(input_scale)

        layers = [inputs]
        conv_layers.insert(0,1)

        connections = []

        filt = Matrix(["\\ddots"])
        filt.scale(filter_scale)

        lines = []

        max_filters = max(conv_layers)

        # Adds conv filter
        for i in range(1,len(conv_layers)):
            filters = VGroup(*[filt.copy() for t in range(conv_layers[i])])
            
            max_scale = max_filters / conv_layers[i] # e.g. 1->128=128/1 or 64->128=128/64
            spacing = max_scale*(filter_spacing+filt.get_height()) - filt.get_height()
            filters.arrange(DOWN,buff=spacing)

            # line = Line([0,0,0],[0,spacing,0],stroke_width=0.5)
            # line.move_to(layers[i].get_center())
            # line.shift([2,0,0])
            # lines.append(line)

            
            filters.move_to(layers[-1].get_center())
            filters.shift([layers[-1].get_width()/2+filters.get_width()/2+layer_spacing,0,0])

            layers.append(filters)

        # Adds conv connections
        for i in range(len(conv_layers)-1):
            next_scale = int(conv_layers[i+1] / conv_layers[i])
            layer_connections = VGroup(*[
                Line(
                    layers[i][k].get_center()+[layers[i][k].get_width()/2,0,0],
                    layers[i+1][next_scale*k+j].get_center()-[layers[i+1][next_scale*k+j].get_width()/2,0,0],
                    stroke_width=0.5
                ) 
                for j in range(next_scale) for k in range(conv_layers[i]) 
            ])
            connections.append(layer_connections)

        # Adds dense layers
        for i in range(len(dense_layers)):
            dense = VGroup(*[Circle(radius=neuron_radius,stroke_color=WHITE,stroke_width=1) for j in range(dense_layers[i])])
            dense.arrange(DOWN,buff=neuron_spacing)

            dense.move_to(layers[-1].get_center())
            dense.shift([layers[-1].get_width()/2+dense.get_width()/2+layer_spacing,0,0])

            layers.append(dense)

            layer_connections = VGroup(*[
                Line(
                    layers[-2][j].get_center()+[layers[-2][j].get_width()/2,0,0],
                    layers[-1][k].get_center()-[layers[-1][k].get_width()/2,0,0],
                    stroke_width=0.5
                ) 
                for j in range(len(layers[-2])) for k in range(len(layers[-1])) 
            ])
            connections.append(layer_connections)

        # lines = VGroup(*lines)
        net = VGroup(VGroup(*layers),VGroup(*connections))
        net.center()
        return net

def setup(scale,h_buff,distance=0.3,buff=0.4):
    # 3x3
    a1 = Matrix([
        [1,1,0],
        [0,1,0],
        [0,1,1]
    ],h_buff=h_buff)
    
    # 1st conv layer
    # ---------------------------------
    # 2x2
    f1 = VGroup(
        Matrix([
            [1,1],
            [0,0]
        ],h_buff=h_buff).set_color(RED),
        Matrix([
            [1,0],
            [0,0]
        ],h_buff=h_buff).set_color(RED)
    )
    f1.arrange(DOWN)

    b1 = VGroup(TexMobject("-2",color=BLUE),TexMobject("-1",color=BLUE))
    b1.arrange(DOWN)

    z1 = VGroup(
        Matrix([
            [0,-1],
            [-1,-1]
        ],h_buff=2*h_buff),
        Matrix([
            [0,0],
            [-1,0]
        ],h_buff=2*h_buff)
    )
    set_layers(z1,distance=distance)
    
    # Can copy bc ReLU is same when all zs >=0
    a2 = VGroup(
        Matrix([
            [0,1],
            [1,1]
        ],h_buff=h_buff),
        Matrix([
            [0,0],
            [1,0]
        ],h_buff=h_buff)
    )
    set_layers(a2,distance=distance)

    # 2nd conv layer
    # ---------------------------------
    # 1x2 (1 rows, 2 cols)
    f2 = VGroup(
        VGroup(
            Matrix([[0,1]],h_buff=h_buff).set_color(RED),
            Matrix([[1,0]],h_buff=h_buff).set_color(RED)
        ),
        VGroup(
            Matrix([[1,0]],h_buff=h_buff).set_color(RED),
            Matrix([[0,1]],h_buff=h_buff).set_color(RED)
        ),
        VGroup(
            Matrix([[1,1]],h_buff=h_buff).set_color(RED),
            Matrix([[1,1]],h_buff=h_buff).set_color(RED)
        )
    )
    for f in f2:
        set_layers(f,distance=distance)
    f2.arrange(DOWN)

    b2 = VGroup(TexMobject("-1",color=BLUE),TexMobject("-1",color=BLUE),TexMobject("-2",color=BLUE))
    b2.arrange(DOWN)

    z2 = VGroup(
        Matrix([
            1,
            2
        ]),
        Matrix([
            0,
            1
        ]),
        Matrix([
            1,
            3
        ])
    )
    set_layers(z2,distance=distance)

    # ReLU
    a3 = z2.copy()

    # 1st dense layer
    # ---------------------------------
    w1 = Matrix([
        [1,0,1,0,1,0],
        [0,1,0,1,0,1]
    ],h_buff=h_buff).set_color(RED)

    b3 = Matrix([-1,-3],h_buff=h_buff).set_color(BLUE)

    z3 = Matrix([1,3])
    a4 = z3.copy() # ReLU

    everything = VGroup(a1,f1,b1,z1,a2,f2,b2,z2,a3,w1,b3,z3,a4)
    everything.arrange(buff=buff)
    everything.scale(scale)

    starting = VGroup(
        a1,f1,
        z1[0][1:3],z1[1][1:3],
        b1,
        a2[0][1:3],a2[1][1:3],
        f2,
        z2[0][1:3],z2[1][1:3],z2[2][1:3],
        b2,
        a3[0][1:3],a3[1][1:3],a3[2][1:3],
        w1,
        z3[1:3],b3,a4[1:3])

    return (a1,f1,b1,z1,a2,f2,b2,z2,a3,w1,b3,z3,a4,everything,starting)

# Convolutional foreprop
class ep2_2(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.2,"Convolutional forepropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))
    
    def play_equations(self,spacing=0.1):
        side_equations = get_equations(equations=[
            r"a^{l+1} = A(z^l)",
            r"z^l = w^l a^l + b^l",
            r"z^l_{i,j} = (a^l * w^l)_{i,j} + b^l", #  
        ],scale=0.5) # 

        title = TextMobject("Convolutional Foreprop")
        title.move_to(side_equations.get_center()+3.3*UP)

        self.play(Write(title))
        self.wait(3)
        self.play(Write(side_equations))
        self.wait(3)
        self.play(Transform(side_equations,side_equations.copy().shift(5*LEFT)))
        self.play(Transform(side_equations,side_equations.copy().shift(0.2*DOWN)))

        return (title,side_equations)

    def play_net(self,side_equations,spacing=0.1):
        net = get_explicit_conv_net((3,3),[(2,2,2),(3,1,2)],[3])
        net.move_to([side_equations.get_x()+side_equations.get_width()/2+net.get_width()/2+spacing,net.get_y(),0])
        self.play(Write(net))
        self.wait(3)
        self.play(ReplacementTransform(net,net.copy().shift(DOWN*2)))

    def play_foreprop(self,side_equations,spacing=0.1,h_buff=0.5,scale=0.4,buff=0.5):
        a1,f1,b1,z1,a2,f2,b2,z2,a3,w1,b3,z3,a4,everything,starting = setup(scale=scale,h_buff=h_buff)

        
        j2 = Matrix([1,1],h_buff=h_buff).set_color(GREY)
        j2.scale(scale)

        everything.move_to([side_equations.get_x()+side_equations.get_width()/2+everything.get_width()/2+spacing,everything.get_y(),0])
        
        base_starting = starting.copy()
        
        self.play(Write(base_starting))
        self.wait()

        everything.shift(2.2*UP)
        self.play(Transform(base_starting,starting))
        everything.shift(2*LEFT)
        self.play(ReplacementTransform(base_starting,starting))

        # Equation highlights
        a = get_highlight_box(side_equations[0][0])
        dense_z = get_highlight_box(side_equations[0][1])
        conv_z = get_highlight_box(side_equations[0][2])

        self.play(Write(conv_z))

        # element_size = (image.get_width()/image_size[0],image.get_height()/image_size[1])
        # shift = (temp.get_width()/2-element_size[0]/2,-temp.get_height()/2+element_size[1]/2,0)

        # z1
        # ----------------------------
        a1_highlight = get_highlight_box(a1,buffer=0.1)
        self.play(Write(a1_highlight))

        f11_highlight = get_highlight_box(f1[0],buffer=0.1)
        self.play(Write(f11_highlight))
        b11_highlight = get_highlight_box(b1[0],buffer=0.1)
        self.play(Write(b11_highlight))
        z11_highlight = get_highlight_box(z1[0],buffer=0.1)
        self.play(Write(z11_highlight))

        j1 = Matrix([[1,1],[1,1]],h_buff=h_buff).set_color(GREY)
        j1.scale(scale)

        calculation = VGroup(a1.copy(),TexMobject("*"),f1[0].copy(),TexMobject("+"),b1[0].copy(),j1,TexMobject("="),z1[0].copy())
        calculation.arrange()

        if calculation.get_x()-calculation.get_width()/2 < side_equations.get_x()+side_equations.get_width()/2:
            calculation.move_to([
                side_equations.get_x()+side_equations.get_width()/2+calculation.get_width()/2+buff,
                calculation.get_y(),
                calculation.get_z()
            ])
        

        self.play(
            Write(calculation[1]),
            Write(calculation[3]),
            Write(calculation[5]),
            Write(calculation[6]),
            Write(calculation[7][1:3])
        )
        self.play(ReplacementTransform(a1.copy(),calculation[0]))
        self.play(ReplacementTransform(f1[0].copy(),calculation[2]))
        self.play(ReplacementTransform(b1[0].copy(),calculation[4]))
        self.play(Write(calculation[7][0]))
        self.play(ReplacementTransform(calculation[7].copy(),z1[0]))

        self.play(
            Uncreate(calculation[2][0]),
            Uncreate(calculation[4][0]),
            Uncreate(calculation[7][0])
        )

        f12_highlight = get_highlight_box(f1[1],buffer=0.1)
        b12_highlight = get_highlight_box(b1[1],buffer=0.1)
        z12_highlight = get_highlight_box(z1[1],buffer=0.1)
        self.play(
            ReplacementTransform(f11_highlight,f12_highlight),
            ReplacementTransform(b11_highlight,b12_highlight),
            ReplacementTransform(z11_highlight,z12_highlight)
        )

        f12copy = f1[1].copy()
        f12copy.move_to(calculation[2])
        self.play(ReplacementTransform(f1[1].copy(),f12copy))

        b12copy = b1[1].copy()
        b12copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b1[1].copy(),b12copy))

        z12copy = z1[1].copy()
        z12copy.move_to(calculation[7].get_center())
        self.play(Write(z12copy))
        self.play(ReplacementTransform(z12copy.copy(),z1[1]))

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
            Uncreate(z12copy)
        )
        self.play(
            Uncreate(b12_highlight),
            Uncreate(f12_highlight)
        )

        # a2
        # ----------------------------

        z1_highlight = get_highlight_box(z1,buffer=0.1)
        a2_highlight = get_highlight_box(a2,buffer=0.1)
        self.play(
            ReplacementTransform(a1_highlight,z1_highlight),
            ReplacementTransform(z12_highlight,a2_highlight),
        )

        conv_z = retainTransform(self,conv_z,a)

        calculation = VGroup(TexMobject("A ("),z1.copy(),TexMobject(")="),a2.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][0][1:3]),
            Write(calculation[3][1][1:3])
        )
        self.play(ReplacementTransform(z1.copy(),calculation[1]))
        self.play(
            Write(calculation[3][0][0]),
            Write(calculation[3][1][0])
        )
        self.play(ReplacementTransform(calculation[3].copy(),a2))
        self.play(Uncreate(calculation))

        # z2
        # ----------------------------

        a = retainTransform(self,a,conv_z)

        z21_highlight = get_highlight_box(z2[0],buffer=0.1)

        self.play(
            Transform(z1_highlight,a2_highlight),
            ReplacementTransform(a2_highlight,z21_highlight)
        )

        f21_highlight = get_highlight_box(f2[0],buffer=0.1)
        b21_highlight = get_highlight_box(b2[0],buffer=0.1)
        self.play(
            Write(f21_highlight),
            Write(b21_highlight)
        )

        j2 = Matrix([1,1],h_buff=h_buff).set_color(GREY)
        j2.scale(scale)

        calculation = VGroup(a2.copy(),TexMobject("*"),f2[0].copy(),TexMobject("+"),b2[0].copy(),j2,TexMobject("="),z2[0].copy())
        calculation.arrange()

        if calculation.get_x()-calculation.get_width()/2 < side_equations.get_x()+side_equations.get_width()/2:
            calculation.move_to([
                side_equations.get_x()+side_equations.get_width()/2+calculation.get_width()/2+buff,
                calculation.get_y(),
                calculation.get_z()
            ])

        self.play(
            Write(calculation[1]),
            Write(calculation[3]),
            Write(calculation[5]),
            Write(calculation[6]),
            Write(calculation[7][1:3])
        )
        self.play(ReplacementTransform(a2.copy(),calculation[0]))
        self.play(ReplacementTransform(f2[0].copy(),calculation[2]))
        self.play(ReplacementTransform(b2[0].copy(),calculation[4]))
        self.play(Write(calculation[7][0]))
        self.play(ReplacementTransform(calculation[7].copy(),z2[0]))

        self.play(
            Uncreate(calculation[2][0][0]),
            Uncreate(calculation[2][1][0]),
            Uncreate(calculation[4][0]),
            Uncreate(calculation[7][0])
        )

        f22_highlight = get_highlight_box(f2[1],buffer=0.1)
        b22_highlight = get_highlight_box(b2[1],buffer=0.1)
        z22_highlight = get_highlight_box(z2[1],buffer=0.1)
        self.play(
            ReplacementTransform(f21_highlight,f22_highlight),
            ReplacementTransform(b21_highlight,b22_highlight),
            ReplacementTransform(z21_highlight,z22_highlight)
        )

        f22copy = f2[1].copy()
        f22copy.move_to(calculation[2])
        self.play(ReplacementTransform(f2[1].copy(),f22copy))

        b22copy = b2[1].copy()
        b22copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b2[1].copy(),b22copy))

        z22copy = z2[1].copy()
        z22copy.move_to(calculation[7].get_center())
        self.play(Write(z22copy[0]))
        self.play(ReplacementTransform(z22copy.copy(),z2[1]))

        self.play(
            Uncreate(f22copy),
            Uncreate(b22copy),
            Uncreate(z22copy[0])
        )

        f23_highlight = get_highlight_box(f2[2],buffer=0.1)
        b23_highlight = get_highlight_box(b2[2],buffer=0.1)
        z23_highlight = get_highlight_box(z2[2],buffer=0.1)
        self.play(
            ReplacementTransform(f22_highlight,f23_highlight),
            ReplacementTransform(b22_highlight,b23_highlight),
            ReplacementTransform(z22_highlight,z23_highlight)
        )

        f23copy = f2[2].copy()
        f23copy.move_to(calculation[2])
        self.play(ReplacementTransform(f2[2].copy(),f23copy))

        b23copy = b2[2].copy()
        b23copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b2[2].copy(),b23copy))

        z23copy = z2[2].copy()
        z23copy.move_to(calculation[7].get_center())
        self.play(Write(z23copy))
        self.play(ReplacementTransform(z23copy.copy(),z2[2]))

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
            Uncreate(z23copy)
        )

        self.play(
            Uncreate(b23_highlight),
            Uncreate(f23_highlight)
        )

        # a3
        # ----------------------------

        z2_highlight = get_highlight_box(z2,buffer=0.1)
        a3_highlight = get_highlight_box(a3,buffer=0.1)
        self.play(
            ReplacementTransform(z1_highlight,z2_highlight),
            ReplacementTransform(z23_highlight,a3_highlight),
        )

        conv_z = retainTransform(self,conv_z,a)

        calculation = VGroup(TexMobject("A ("),z2.copy(),TexMobject(")="),a3.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][0][1:3]),
            Write(calculation[3][1][1:3]),
            Write(calculation[3][2][1:3])
        )
        self.play(ReplacementTransform(z2.copy(),calculation[1]))
        self.play(
            Write(calculation[3][0][0]),
            Write(calculation[3][1][0]),
            Write(calculation[3][2][0])
        )
        self.play(ReplacementTransform(calculation[3].copy(),a3))
        self.play(Uncreate(calculation))

        # z3
        # ----------------------------

        z3_highlight = get_highlight_box(z3,buffer=0.1)

        w1_highlight = get_highlight_box(w1,buffer=0.1)
        b3_highlight = get_highlight_box(b3,buffer=0.1)

        self.play(
            Transform(z2_highlight,a3_highlight),
            ReplacementTransform(a3_highlight,z3_highlight)
        )
        self.play(
            Write(w1_highlight),
            Write(b3_highlight)
        )

        a = retainTransform(self,a,dense_z)

        flat = VGroup(a3[0].copy(),a3[1].copy(),a3[2].copy())
        flat.arrange(DOWN,buff=0.05)

        calculation = VGroup(w1.copy(),flat,TexMobject("+"),b3.copy(),TexMobject("="),z3.copy())
        calculation.arrange()

        flattened = Matrix([2,1,3,2,5,3],h_buff=h_buff)
        flattened.scale(scale)
        flattened.move_to(flat.get_center())

        self.play(
            Write(calculation[2]),
            Write(calculation[4]),
            Write(calculation[5][1:3])
        )

        self.play(ReplacementTransform(a3[0].copy(),flat[0]))
        self.play(ReplacementTransform(a3[1].copy(),flat[1]))
        self.play(ReplacementTransform(a3[2].copy(),flat[2]))
        l_brackets = VGroup(flat[0][1],flat[1][1],flat[2][1])
        r_brackets = VGroup(flat[0][2],flat[1][2],flat[2][2])
        self.play(
            ReplacementTransform(l_brackets,flattened[1]),
            ReplacementTransform(r_brackets,flattened[2])
        )

        self.play(
            ReplacementTransform(w1.copy(),calculation[0]),
            ReplacementTransform(b3.copy(),calculation[3])
        )
        
        self.play(Write(calculation[5][0]))
        self.play(ReplacementTransform(calculation[5].copy(),z3))
        self.play(
            Uncreate(calculation[0]),
            Uncreate(flattened[1:3]),
            Uncreate(flat[0][0]),
            Uncreate(flat[1][0]),
            Uncreate(flat[2][0]),
            Uncreate(calculation[2:6])
        )
        self.play(
            Uncreate(w1_highlight),
            Uncreate(b3_highlight)
        )

        # a3
        # ----------------------------

        a4_highlight = get_highlight_box(a4,buffer=0.1)
        self.play(
            Transform(z2_highlight,z3_highlight),
            ReplacementTransform(z3_highlight,a4_highlight)
        )

        dense_z = retainTransform(self,dense_z,a)

        calculation = VGroup(TexMobject("A ("),z3.copy(),TexMobject(")="),a4.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][1:3])
        )
        self.play(ReplacementTransform(z3.copy(),calculation[1]))
        self.play(Write(calculation[3][0]))
        self.play(ReplacementTransform(calculation[3].copy(),a4))
        
    def construct(self):
        self.play_intro()

        title,side_equations = self.play_equations()

        self.play_net(side_equations)

        self.play_foreprop(side_equations)
        self.wait(3)

# side_equations = get_equations(equations=[
# r"\delta^L = \nabla_a C \odot A'(z^L)",
# r"\delta^l = (w^{l+1})^T \delta^{l+1} \odot A'(z^l)",
# r"\frac{\partial C}{\partial b^l} = \delta^l",
# r"\frac{\partial C}{\partial w^l} = \delta^l (a^l)^T"
# ], wheres=[r"\delta^l = \frac{\partial C}{\partial z^l}"])

# Convolutional backprop
class ep2_3(Scene):
    def play_intro(self):
        title_scene = get_title_screen(2.3,"Convolutional backpropagation")

        self.add(title_scene)
        self.wait(2)
        self.play(Uncreate(title_scene))
    
    def play_equations(self,spacing=0.1):
        side_equations = get_equations(equations=[
            r"a^{l+1} = A(z^l)",
            r"z^l = w^l a^l + b^l",
            r"\delta^L = \nabla_a C \odot A'(z^L)",
            r"\delta^l = a",
            r"\frac{\partial C}{\partial b^l} = \delta^l",
            r"\frac{\partial C}{\partial w^l_{m,n}} = \delta_l \odot \frac{\partial z^l}{\partial w^l}", #  
        ], wheres=[r"\delta_l = \frac{\partial C}{\partial z^l}"],scale=0.5) # 

        title = TextMobject("Convolutional Foreprop")
        title.move_to(side_equations.get_center()+3.3*UP)

        self.play(Write(title))
        self.wait(3)
        self.play(Write(side_equations))
        self.wait(3)
        self.play(Transform(side_equations,side_equations.copy().shift(5*LEFT)))
        self.play(Transform(side_equations,side_equations.copy().shift(0.2*DOWN)))

        return (title,side_equations)

    def play_net(self,side_equations,spacing=0.1):
        net = get_explicit_conv_net((3,3),[(2,2,2),(3,1,2)],[3])
        net.move_to([side_equations.get_x()+side_equations.get_width()/2+net.get_width()/2+spacing,net.get_y(),0])
        self.play(Write(net))
        self.wait(3)
        self.play(ReplacementTransform(net,net.copy().shift(DOWN*2)))

    def play_foreprop(self,side_equations,spacing=0.1,h_buff=0.5,scale=0.4,buff=0.5):
        a1,f1,b1,z1,a2,f2,b2,z2,a3,w1,b3,z3,a4,everything,starting = setup(scale=scale,h_buff=h_buff)

        
        j2 = Matrix([1,1],h_buff=h_buff).set_color(GREY)
        j2.scale(scale)

        everything.move_to([side_equations.get_x()+side_equations.get_width()/2+everything.get_width()/2+spacing,everything.get_y(),0])
        
        base_starting = starting.copy()
        
        self.play(Write(base_starting))
        self.wait()

        everything.shift(2.2*UP)
        self.play(Transform(base_starting,starting))
        everything.shift(2*LEFT)
        self.play(ReplacementTransform(base_starting,starting))

        # Equation highlights
        a = get_highlight_box(side_equations[0][0])
        dense_z = get_highlight_box(side_equations[0][1])
        conv_z = get_highlight_box(side_equations[0][2])

        self.play(Write(conv_z))

        # element_size = (image.get_width()/image_size[0],image.get_height()/image_size[1])
        # shift = (temp.get_width()/2-element_size[0]/2,-temp.get_height()/2+element_size[1]/2,0)

        # z1
        # ----------------------------
        a1_highlight = get_highlight_box(a1,buffer=0.1)
        self.play(Write(a1_highlight))

        f11_highlight = get_highlight_box(f1[0],buffer=0.1)
        self.play(Write(f11_highlight))
        b11_highlight = get_highlight_box(b1[0],buffer=0.1)
        self.play(Write(b11_highlight))
        z11_highlight = get_highlight_box(z1[0],buffer=0.1)
        self.play(Write(z11_highlight))

        j1 = Matrix([[1,1],[1,1]],h_buff=h_buff).set_color(GREY)
        j1.scale(scale)

        calculation = VGroup(a1.copy(),TexMobject("*"),f1[0].copy(),TexMobject("+"),b1[0].copy(),j1,TexMobject("="),z1[0].copy())
        calculation.arrange()

        if calculation.get_x()-calculation.get_width()/2 < side_equations.get_x()+side_equations.get_width()/2:
            calculation.move_to([
                side_equations.get_x()+side_equations.get_width()/2+calculation.get_width()/2+buff,
                calculation.get_y(),
                calculation.get_z()
            ])
        

        self.play(
            Write(calculation[1]),
            Write(calculation[3]),
            Write(calculation[5]),
            Write(calculation[6]),
            Write(calculation[7][1:3])
        )
        self.play(ReplacementTransform(a1.copy(),calculation[0]))
        self.play(ReplacementTransform(f1[0].copy(),calculation[2]))
        self.play(ReplacementTransform(b1[0].copy(),calculation[4]))
        self.play(Write(calculation[7][0]))
        self.play(ReplacementTransform(calculation[7].copy(),z1[0]))

        self.play(
            Uncreate(calculation[2][0]),
            Uncreate(calculation[4][0]),
            Uncreate(calculation[7][0])
        )

        f12_highlight = get_highlight_box(f1[1],buffer=0.1)
        b12_highlight = get_highlight_box(b1[1],buffer=0.1)
        z12_highlight = get_highlight_box(z1[1],buffer=0.1)
        self.play(
            ReplacementTransform(f11_highlight,f12_highlight),
            ReplacementTransform(b11_highlight,b12_highlight),
            ReplacementTransform(z11_highlight,z12_highlight)
        )

        f12copy = f1[1].copy()
        f12copy.move_to(calculation[2])
        self.play(ReplacementTransform(f1[1].copy(),f12copy))

        b12copy = b1[1].copy()
        b12copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b1[1].copy(),b12copy))

        z12copy = z1[1].copy()
        z12copy.move_to(calculation[7].get_center())
        self.play(Write(z12copy))
        self.play(ReplacementTransform(z12copy.copy(),z1[1]))

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
            Uncreate(z12copy)
        )
        self.play(
            Uncreate(b12_highlight),
            Uncreate(f12_highlight)
        )

        # a2
        # ----------------------------

        z1_highlight = get_highlight_box(z1,buffer=0.1)
        a2_highlight = get_highlight_box(a2,buffer=0.1)
        self.play(
            ReplacementTransform(a1_highlight,z1_highlight),
            ReplacementTransform(z12_highlight,a2_highlight),
        )

        conv_z = retainTransform(self,conv_z,a)

        calculation = VGroup(TexMobject("A ("),z1.copy(),TexMobject(")="),a2.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][0][1:3]),
            Write(calculation[3][1][1:3])
        )
        self.play(ReplacementTransform(z1.copy(),calculation[1]))
        self.play(
            Write(calculation[3][0][0]),
            Write(calculation[3][1][0])
        )
        self.play(ReplacementTransform(calculation[3].copy(),a2))
        self.play(Uncreate(calculation))

        # z2
        # ----------------------------

        a = retainTransform(self,a,conv_z)

        z21_highlight = get_highlight_box(z2[0],buffer=0.1)

        self.play(
            Transform(z1_highlight,a2_highlight),
            ReplacementTransform(a2_highlight,z21_highlight)
        )

        f21_highlight = get_highlight_box(f2[0],buffer=0.1)
        b21_highlight = get_highlight_box(b2[0],buffer=0.1)
        self.play(
            Write(f21_highlight),
            Write(b21_highlight)
        )

        j2 = Matrix([1,1],h_buff=h_buff).set_color(GREY)
        j2.scale(scale)

        calculation = VGroup(a2.copy(),TexMobject("*"),f2[0].copy(),TexMobject("+"),b2[0].copy(),j2,TexMobject("="),z2[0].copy())
        calculation.arrange()

        if calculation.get_x()-calculation.get_width()/2 < side_equations.get_x()+side_equations.get_width()/2:
            calculation.move_to([
                side_equations.get_x()+side_equations.get_width()/2+calculation.get_width()/2+buff,
                calculation.get_y(),
                calculation.get_z()
            ])

        self.play(
            Write(calculation[1]),
            Write(calculation[3]),
            Write(calculation[5]),
            Write(calculation[6]),
            Write(calculation[7][1:3])
        )
        self.play(ReplacementTransform(a2.copy(),calculation[0]))
        self.play(ReplacementTransform(f2[0].copy(),calculation[2]))
        self.play(ReplacementTransform(b2[0].copy(),calculation[4]))
        self.play(Write(calculation[7][0]))
        self.play(ReplacementTransform(calculation[7].copy(),z2[0]))

        self.play(
            Uncreate(calculation[2][0][0]),
            Uncreate(calculation[2][1][0]),
            Uncreate(calculation[4][0]),
            Uncreate(calculation[7][0])
        )

        f22_highlight = get_highlight_box(f2[1],buffer=0.1)
        b22_highlight = get_highlight_box(b2[1],buffer=0.1)
        z22_highlight = get_highlight_box(z2[1],buffer=0.1)
        self.play(
            ReplacementTransform(f21_highlight,f22_highlight),
            ReplacementTransform(b21_highlight,b22_highlight),
            ReplacementTransform(z21_highlight,z22_highlight)
        )

        f22copy = f2[1].copy()
        f22copy.move_to(calculation[2])
        self.play(ReplacementTransform(f2[1].copy(),f22copy))

        b22copy = b2[1].copy()
        b22copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b2[1].copy(),b22copy))

        z22copy = z2[1].copy()
        z22copy.move_to(calculation[7].get_center())
        self.play(Write(z22copy[0]))
        self.play(ReplacementTransform(z22copy.copy(),z2[1]))

        self.play(
            Uncreate(f22copy),
            Uncreate(b22copy),
            Uncreate(z22copy[0])
        )

        f23_highlight = get_highlight_box(f2[2],buffer=0.1)
        b23_highlight = get_highlight_box(b2[2],buffer=0.1)
        z23_highlight = get_highlight_box(z2[2],buffer=0.1)
        self.play(
            ReplacementTransform(f22_highlight,f23_highlight),
            ReplacementTransform(b22_highlight,b23_highlight),
            ReplacementTransform(z22_highlight,z23_highlight)
        )

        f23copy = f2[2].copy()
        f23copy.move_to(calculation[2])
        self.play(ReplacementTransform(f2[2].copy(),f23copy))

        b23copy = b2[2].copy()
        b23copy.move_to(calculation[4].get_center())
        self.play(ReplacementTransform(b2[2].copy(),b23copy))

        z23copy = z2[2].copy()
        z23copy.move_to(calculation[7].get_center())
        self.play(Write(z23copy))
        self.play(ReplacementTransform(z23copy.copy(),z2[2]))

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
            Uncreate(z23copy)
        )

        self.play(
            Uncreate(b23_highlight),
            Uncreate(f23_highlight)
        )

        # a3
        # ----------------------------

        z2_highlight = get_highlight_box(z2,buffer=0.1)
        a3_highlight = get_highlight_box(a3,buffer=0.1)
        self.play(
            ReplacementTransform(z1_highlight,z2_highlight),
            ReplacementTransform(z23_highlight,a3_highlight),
        )

        conv_z = retainTransform(self,conv_z,a)

        calculation = VGroup(TexMobject("A ("),z2.copy(),TexMobject(")="),a3.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][0][1:3]),
            Write(calculation[3][1][1:3]),
            Write(calculation[3][2][1:3])
        )
        self.play(ReplacementTransform(z2.copy(),calculation[1]))
        self.play(
            Write(calculation[3][0][0]),
            Write(calculation[3][1][0]),
            Write(calculation[3][2][0])
        )
        self.play(ReplacementTransform(calculation[3].copy(),a3))
        self.play(Uncreate(calculation))

        # z3
        # ----------------------------

        z3_highlight = get_highlight_box(z3,buffer=0.1)

        w1_highlight = get_highlight_box(w1,buffer=0.1)
        b3_highlight = get_highlight_box(b3,buffer=0.1)

        self.play(
            Transform(z2_highlight,a3_highlight),
            ReplacementTransform(a3_highlight,z3_highlight)
        )
        self.play(
            Write(w1_highlight),
            Write(b3_highlight)
        )

        a = retainTransform(self,a,dense_z)

        flat = VGroup(a3[0].copy(),a3[1].copy(),a3[2].copy())
        flat.arrange(DOWN,buff=0.05)

        calculation = VGroup(w1.copy(),flat,TexMobject("+"),b3.copy(),TexMobject("="),z3.copy())
        calculation.arrange()

        flattened = Matrix([2,1,3,2,5,3],h_buff=h_buff)
        flattened.scale(scale)
        flattened.move_to(flat.get_center())

        self.play(
            Write(calculation[2]),
            Write(calculation[4]),
            Write(calculation[5][1:3])
        )

        self.play(ReplacementTransform(a3[0].copy(),flat[0]))
        self.play(ReplacementTransform(a3[1].copy(),flat[1]))
        self.play(ReplacementTransform(a3[2].copy(),flat[2]))
        l_brackets = VGroup(flat[0][1],flat[1][1],flat[2][1])
        r_brackets = VGroup(flat[0][2],flat[1][2],flat[2][2])
        self.play(
            ReplacementTransform(l_brackets,flattened[1]),
            ReplacementTransform(r_brackets,flattened[2])
        )

        self.play(
            ReplacementTransform(w1.copy(),calculation[0]),
            ReplacementTransform(b3.copy(),calculation[3])
        )
        
        self.play(Write(calculation[5][0]))
        self.play(ReplacementTransform(calculation[5].copy(),z3))
        self.play(
            Uncreate(calculation[0]),
            Uncreate(flattened[1:3]),
            Uncreate(flat[0][0]),
            Uncreate(flat[1][0]),
            Uncreate(flat[2][0]),
            Uncreate(calculation[2:6])
        )
        self.play(
            Uncreate(w1_highlight),
            Uncreate(b3_highlight)
        )

        # a3
        # ----------------------------

        a4_highlight = get_highlight_box(a4,buffer=0.1)
        self.play(
            Transform(z2_highlight,z3_highlight),
            ReplacementTransform(z3_highlight,a4_highlight)
        )

        dense_z = retainTransform(self,dense_z,a)

        calculation = VGroup(TexMobject("A ("),z3.copy(),TexMobject(")="),a4.copy())
        calculation.arrange()

        self.play(
            Write(calculation[0]),
            Write(calculation[2]),
            Write(calculation[3][1:3])
        )
        self.play(ReplacementTransform(z3.copy(),calculation[1]))
        self.play(Write(calculation[3][0]))
        self.play(ReplacementTransform(calculation[3].copy(),a4))
        
    def construct(self):
        self.play_intro()

        title,side_equations = self.play_equations()

        self.play_net(side_equations)

        self.play_foreprop(side_equations)
        self.wait(3)

# TODO
# - Dilation
# - Group convulution