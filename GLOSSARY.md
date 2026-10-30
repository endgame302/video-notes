# video-notes

An agent skill that turns a video into study notes someone can learn from without watching it.

## Language

**Notes**:
The content written from a video: what it teaches, in the video's order.
_Avoid_: Summary, write-up

**Page**:
The delivered HTML document that carries the notes.
_Avoid_: Notes (when the HTML itself is meant), output

**Note quality**:
How well someone can learn from the notes, and do what the video teaches, without watching it.
_Avoid_: Coverage, accuracy (as a stand-in for the whole)

**On-screen state**:
One distinct thing a video shows, such as a slide, a page, an overlay or a code screen at a new step.
_Avoid_: Scene, shot

**Capture coverage**:
The share of a video's on-screen states with at least one kept frame.
_Avoid_: Coverage (unqualified)

**Transcript coverage**:
The share of a video's transcript chunks that map to a section of the notes.
_Avoid_: Coverage (unqualified)
