from manim import *

# Episodes are numbered with major and minor numbers (e.g. 1.x covers dense nets (func names being 1_0,1_1,etc.), 2.x covers conv nets)
# Utility functions are defined just before the 1st episode in which they are used

# Gets title screen
def get_title_screen(episodeNumber, episodeDescription):
    super_title = Text("A little more than an introduction to:")
    super_title.scale(0.75)
    title = Text("Neural Networks")
    title.scale(2)
    subtitle = Text("Episode " + str(episodeNumber) + ": " + episodeDescription)
    subtitle.scale(0.75)
    title_scene = VGroup(super_title, title, subtitle)
    title_scene.arrange(DOWN, buff=1)

    return title_scene


# Creates a box of a bunch of equations
def get_equations(equations, wheres=[], buffer=1, scale=0.5, where_scale=0.8):
    equation_box = [
        MathTex(str(i + 1) + r". \hspace{6pt}", eqStr)
        for (i, eqStr) in enumerate(equations)
    ]

    if len(wheres) > 0:
        wheresList = [r"Where: \hspace{6pt}"]
        for (i, eqStr) in enumerate(wheres):
            wheresList.append(eqStr)
            if i != len(wheres) - 1:  # For all but last element add `,` after
                wheresList.append(", ")

        wheresTex = MathTex(*wheresList)
        wheresTex.scale(where_scale)
        equation_box.append(wheresTex)

    equation_box = VGroup(*equation_box)

    equation_box.arrange(DOWN, buff=0.75)

    align_pos_x = equation_box.get_center()[0] - equation_box.get_width() / 2 + buffer
    for eq in equation_box:
        eq.move_to([align_pos_x + eq.get_width() / 2, eq.get_y(), eq.get_z()])

    border = Rectangle(
        height=equation_box.get_height() + 1, width=equation_box.get_width() + 1
    )
    border.move_to(equation_box.get_center())

    equation_box = VGroup(equation_box, border)
    equation_box.scale(scale)
    equation_box.center()

    return equation_box


# Gets yellow box around thing
def get_highlight_box(x, buffer=0.2, stroke_width=2):
    box = Rectangle(
        stroke_width=stroke_width,
        color=YELLOW,
        height=x.get_height() + buffer,
        width=x.get_width() + buffer,
    )
    box.move_to(x.get_center())
    return box


# Transforms `a` -> `b`.
# Returns original value of `a`.
def retainTransform(scene, a, b):
    copy = a.copy()
    scene.play(ReplacementTransform(a, b))
    return copy


# Scales a given `obj` from an original scale `old` to a new scale `new`
def rescale(obj, old, new):
    obj.scale(1 / old)
    obj.scale(new)
    return obj


# side_equations = get_equations(equations=[
# r"\delta^L = \nabla_a C \odot A'(z^L)",
# r"\delta^l = (w^{l+1})^T \delta^{l+1} \odot A'(z^l)",
# r"\frac{\partial C}{\partial b^l} = \delta^l",
# r"\frac{\partial C}{\partial w^l} = \delta^l (a^l)^T"
# ], wheres=[r"\delta^l = \frac{\partial C}{\partial z^l}"])

# TODO
# - Dilation
# - Group convulution
