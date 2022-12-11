import sys, os

sys.path.append(os.path.abspath(os.path.join("..")))

from scommon import (
    get_title_screen,
    SCENE_WAIT,
    get_equations,
    get_highlight_box,
    rescale,
    retainTransform,
)
from manim import *

# Gets an xor net
def get_xor_net(text_scale, vertical_spacing, horizontal_spacing):
    inputs = VGroup(
        *[Circle(radius=0.15, stroke_color=WHITE, stroke_width=1) for i in range(0, 2)]
    )
    inputs.arrange(DOWN, buff=vertical_spacing)
    hidden = VGroup(
        *[Circle(radius=0.15, stroke_color=WHITE, stroke_width=1) for i in range(0, 3)]
    )
    hidden.arrange(DOWN, buff=vertical_spacing)
    outputs = VGroup(
        VGroup(Circle(radius=0.15, stroke_color=WHITE, stroke_width=1), Text("False")),
        VGroup(Circle(radius=0.15, stroke_color=WHITE, stroke_width=1), Text("True")),
    )
    for group in outputs:
        group[1].scale(text_scale)
        group.arrange()
    outputs.arrange(DOWN, buff=vertical_spacing)

    neurons = VGroup(inputs, hidden, outputs)
    neurons.arrange(buff=horizontal_spacing)

    input_edges = VGroup(
        *[
            Line(n1.get_center(), n2[0].get_center(), stroke_width=0.5)
            for n1 in inputs
            for n2 in hidden
        ]
    )
    output_edges = VGroup(
        *[
            Line(n1.get_center(), n2[0].get_center(), stroke_width=0.5)
            for n1 in hidden
            for n2 in outputs
        ]
    )

    connections = VGroup(input_edges, output_edges)

    return VGroup(neurons, connections)