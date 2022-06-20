from discord.ext import commands

from Plugin import AutomataPlugin
from Utils import send_code_block_maybe_as_file


class FSM(AutomataPlugin):
    """
    Emulates a FSM.
    """

    @commands.command()
    async def fsm(self, ctx: commands.Context, code: str):
        """
        Emulates a FSM. Wrap the code in quotes, with each statement on it's own line.

        Statements:
        t x y z: Define a transition from state x to state z when getting an input of y.
        i x: Defines state x as the initial state.
        a x1 x2 x3...: Sets all the given states to accepting states.
        d x1 x2 x3...: Adds all given data to the list of input data to process over.
        """
        transitions = {}
        data = []
        state = None
        accepting = []
        for line in code.split("\n"):
            tokens = line.split(" ")
            if tokens[0] == "t":
                if tokens[1] not in transitions:
                    transitions[tokens[1]] = {}
                transitions[tokens[1]][tokens[2]] = tokens[3]
            elif tokens[0] == "d":
                for token in tokens[1:]:
                    data.append(token)
            elif tokens[0] == "i":
                state = tokens[1]
            elif tokens[0] == "a":
                for token in tokens[1:]:
                    accepting.append(token)

        if not state:
            await ctx.send("FSM crashed: no initial state specified")
            return

        iterations = 0

        changes = []
        while len(data) != 0 or iterations >= 1000:
            iterations += 1
            token = data[0]
            data.remove(token)

            try:
                changes.append(f"{state} -> {transitions[state][token]} ({token})")
                state = transitions[state][token]
            except KeyError:
                changes.append(
                    f"FSM crashed: no transition for state {state} and input {token}"
                )
                break

        if iterations >= 1000:
            changes.append(
                "FSM haulted: more than 1000 iterations; maybe infinite loop?"
            )
        else:
            if state in accepting:
                changes.append("FSM accepted")
            else:
                changes.append("FSM rejected")

        message = "\n".join(changes)

        await send_code_block_maybe_as_file(ctx, message)
