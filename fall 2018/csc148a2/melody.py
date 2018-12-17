"""CSC148 Assignment 2: Music helper library

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains some helpers used to convert between our integer-based
representation of melodies and different music file formats.

You should not change anything in this file.
"""
import io
from typing import List, Tuple

import mido as mido
import pygame as pg


class Melody:
    """A class representing a melody.

    === Attributes ===
    name: the name of the melody
    notes: a sequence of notes representing the melody.
        A *note* is a tuple of two integers:
          - the first is an integer between 21 and 108, representing the pitch
          - the second is an integer representing the duration of the note,
            in milliseconds

    Note: you can find a chart showing the conversion between integers and
    standard note names at http://newt.phys.unsw.edu.au/jw/notes.html.
    """
    name: str
    notes: List[Tuple[int, int]]

    def __init__(self, name: str, notes: List[Tuple[int, int]]) -> None:
        """Initialize a new melody with the given name and notes."""
        self.name = name
        self.notes = notes

    def play(self) -> None:
        """Play this melody (make sure your computer's speakers are on!)."""
        play_midi_sequence(self.notes)


def play_midi_sequence(notes: List[Tuple[int, int]]) -> None:
    """Given a list of notes, create a MIDI file and play it.
    """
    f = create_midi_file(notes)
    play_midi_file(f)


def play_midi_file(midi_file: io.BytesIO) -> None:
    """Given a file (or file-like) MIDI object, play it using pygame.
    """
    pg.mixer.init()
    pg.mixer.music.load(midi_file)
    pg.mixer.music.play()

    while pg.mixer.music.get_busy():
        pg.time.Clock().tick(10)


def create_midi_file(notes: List[Tuple[int, int]]) -> io.BytesIO:
    """Create a MIDI file from the given list of notes.

    Notes are played with piano instrument.
    """
    byte_stream = io.BytesIO()

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for note, t in notes:
        track.append(mido.Message('note_on', note=note, velocity=64))
        track.append(mido.Message('note_off', note=note, time=t))

    mid.save(file=byte_stream)

    return io.BytesIO(byte_stream.getvalue())
