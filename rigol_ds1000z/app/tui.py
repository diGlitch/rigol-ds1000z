from textual import events
from textual.app import App
from textual.widgets import Footer, Placeholder

from rigol_ds1000z import Rigol_DS1000Z, find_visa


class Rigol_DS100Z_TUI(App):
    async def on_mount(self, event: events.Mount) -> None:
        grid = await self.view.dock_grid()

        grid.add_column(name="ch1-col")
        grid.add_column(name="ch2-col")
        grid.add_column(name="ch3-col")
        grid.add_column(name="ch4-col")

        grid.add_row(name="horiz-row")
        grid.add_row(name="vert-row")
        grid.add_row(name="console-row", fraction=0, min_size=3)
        grid.add_row(name="footer-row", fraction=0, min_size=1)

        grid.add_areas(display="ch1-col,horiz-row")
        grid.add_areas(waveform="ch2-col,horiz-row")
        grid.add_areas(timebase="ch3-col,horiz-row")
        grid.add_areas(trigger="ch4-col,horiz-row")
        grid.add_areas(vert_ch1="ch1-col,vert-row")
        grid.add_areas(vert_ch2="ch2-col,vert-row")
        grid.add_areas(vert_ch3="ch3-col,vert-row")
        grid.add_areas(vert_ch4="ch4-col,vert-row")
        grid.add_areas(console="ch1-col-start|ch4-col-end,console-row")
        grid.add_areas(footer="ch1-col-start|ch4-col-end,footer-row")

        grid.place(
            display=Placeholder(name="DISPLAY"),
            waveform=Placeholder(name="WAVEFORM"),
            timebase=Placeholder(name="TIMEBASE"),
            trigger=Placeholder(name="TRIGGER"),
            vert_ch1=Placeholder(name="CH1"),
            vert_ch2=Placeholder(name="CH2"),
            vert_ch3=Placeholder(name="CH3"),
            vert_ch4=Placeholder(name="CH4"),
            console=Placeholder(name="CONSOLE"),
            footer=Footer(),
        )

    async def on_load(self) -> None:
        await self.bind("q", "quit", "Quit")
        await self.bind("r", "refresh", "Refresh")
        await self.bind("1", "channel1", "Ch1")
        await self.bind("2", "channel2", "Ch2")
        await self.bind("3", "channel3", "Ch3")
        await self.bind("4", "channel4", "Ch4")
        await self.bind("c", "clear", "Clear")
        await self.bind("a", "autoscale", "Auto")
        await self.bind("s", "runstop", "Run/Stop")
        await self.bind("i", "single", "Single")
        await self.bind("f", "force", "Force")
        await self.bind("d", "display", "Display")
        await self.bind("w", "waveform", "Waveform")

        self.oscope = Rigol_DS1000Z(visa=find_visa()).open()

    async def action_refresh(self) -> None:
        # TODO: update all widgets with latest settings
        pass

    async def action_quit(self) -> None:
        self.oscope.close()
        await super().action_quit()

    async def action_channel1(self) -> None:
        is_active = not self.oscope.channel(n=1).display
        self.oscope.channel(n=1, display=is_active)

    async def action_channel2(self) -> None:
        is_active = not self.oscope.channel(n=2).display
        self.oscope.channel(n=2, display=is_active)

    async def action_channel3(self) -> None:
        is_active = not self.oscope.channel(n=3).display
        self.oscope.channel(n=3, display=is_active)

    async def action_channel4(self) -> None:
        is_active = not self.oscope.channel(n=4).display
        self.oscope.channel(n=4, display=is_active)

    async def action_clear(self) -> None:
        self.oscope.clear()

    async def action_autoscale(self) -> None:
        self.oscope.autoscale()

    async def action_runstop(self) -> None:
        # TODO: check trigger status, toggle run/stop
        pass

    async def action_single(self) -> None:
        self.oscope.single()

    async def action_force(self) -> None:
        self.oscope.tforce()

    async def action_display(self) -> None:
        # TODO: capture the oscope display and screenshot the tui
        pass

    async def action_waveform(self) -> None:
        # TODO: save all the waveforms with active channel displays
        pass


def run():
    Rigol_DS100Z_TUI.run(title="rigol-ds1000z")
