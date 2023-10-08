from contextlib import suppress
from ..key_event import KeyEvent


class State:
    """a game state."""

    def __init__(self):
        self.parent = None
        self.stack = []

    def on_enter(self):
        """Called when this state was entered. Initialize resources here, and call the super classes enter() too."""
        for state in self.stack:
            state.enter()

    def on_pop(self):
        """Called after this state is popped off the parrent state's stack. Destroy any resources asociated with this state and call the super classes pop() method"""
        for state in self.stack:
            state.on_pop()

    def update(self, key_events: list[KeyEvent]) -> None:
        """Called on each tick of the game loop. key_events contains a list of key events since the last frame. Call the super classes update() method if you overwride this method"""
        # Update the last state on the stack of substates
        if self.stack:
            self.stack[-1].update(key_events)

    def append(self, state):
        """Append a state to this states stack. Returns the state that was appended"""
        self.stack.append(state)
        state.parent = self
        state.on_enter()
        return state

    def pop(self):
        """pop the last state from this state's stack. Raise IndexError if empty."""
        state = self.stack.pop()
        state.on_pop()
        state.parent = None
        return state

    def replace_last_substate(self, state):
        """Pop the stack and append [state] in its place. Does not raise an exception if the stack is empty, instead appending [state] as the first item. Returns the state that was appended."""
        with suppress(IndexError):
            self.pop()
        return self.append(state)

    def get_root_state(self):
        """Returns the root state, which is almost always an instance of punch.game.Game. It is safe to use that anywhere after on_enter() was called, so after you append the state. It is ok, and you should, use this method to get a referense to the top level frame to do whatever you want with it or if you have global state."""
        return self if self.parent is None else self.parent.get_root_state()
