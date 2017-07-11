#!/usr/bin/env python3
from agent import *
from piece import *
from core import *
from debug import *
from waste_makes_haste import *

def get_envy_free_allocation(agents, piece, get_call_number=False, fractalize=True):
    Piece.piece_counter = 0
    Agent.agent_counter = 0
    agents = agents[:]
    #We will be updating each agent's allocated cake throughout the algorithm
    allocated_cake = [a.allocated_cake for a in agents]
    residue = piece
    for i in range(100):
        debug_print(' ',i,' Agent count:',len(agents))
        cutter = agents[ i % len(agents) ]
        other_agents = [a for a in agents if a != cutter]

        #Run core and get the updated residue
        pieces = core(cutter, agents, residue)
        residue = Piece.extract_residue_from_pieces(pieces)

        ### add to player's allocations
        for p in pieces:
            p.allocated.allocated_cake += p

        # Check if residue is None. If so, return envy free allocation! Also return if the residue is full of empty intervals
        if Piece.is_empty(residue):
            return i+1 if get_call_number else allocated_cake

        # See if we can reduce the number of players using a dominating set
        dominating_set = Agent.get_dominating_set(agents, allocated_cake, residue)
        if dominating_set != None:
            dominated = list(dominating_set[1])
            agents = dominated

        #Fractalize the player preferences
        if fractalize:
            for a in agents:
                a.fractalize_preferences(residue.intervals)

def get_waste_makes_haste_envy_free_allocation(agents, piece, get_call_number=False, fractalize=True):
    Piece.piece_counter = 0
    Agent.agent_counter = 0
    agents = agents[:]
    #We will be updating each agent's allocated cake throughout the algorithm
    allocated_cake = [a.allocated_cake for a in agents]
    residue = piece
    for i in range(100):
        debug_print(' ',i,' Agent count:',len(agents))

        #Run core and get the updated residue
        pieces = get_waste_makes_haste_allocation(agents, residue)
        residue = sum([p for p in pieces if p.allocated==None], Piece([]))

        ### add to player's allocations
        for p in pieces:
            if p.allocated != None:
                p.allocated.allocated_cake += p

        # Check if residue is None. If so, return envy free allocation! Also return if the residue is full of empty intervals
        if Piece.is_empty(residue):
            return i+1 if get_call_number else allocated_cake

        # See if we can reduce the number of players using a dominating set
        dominating_set = Agent.get_dominating_set(agents, allocated_cake, residue)
        if dominating_set != None:
            dominated = list(dominating_set[1])
            agents = dominated

        #Fractalize the player preferences
        if fractalize:
            for a in agents:
                a.fractalize_preferences(residue.intervals)

if __name__ == '__main__':
    for i in range(6):
        print()
        print(i)
        agents = [Agent() for i in range(4)]
        pieces = get_waste_makes_haste_envy_free_allocation(agents, Piece.get_whole_piece())

        assert envy_free(pieces)
