# -*- coding: utf-8 -*-

# Copyright (C) <2015> Markus Hackspacher

# This file is part of villager-sim.

# villager-sim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# villager-sim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with villager-sim.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import pep8


class TestCodeFormat(unittest.TestCase):
    """
    Test of the code format
    """

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['Builder.py',
                                        'Building.py',
                                        'Clips.py',
                                        'Entities.py',
                                        'Farmer.py',
                                        'GameEntity.py',
                                        'Image_funcs.py',
                                        'Lumberjack.py',
                                        'New_Icon.py',
                                        'NewVillagerSim.py',
                                        'StateMachine.py',
                                        'Tile.py',
                                        'Villager.py',
                                        'World.py',
                                        'Tests/test_pep8.py',
                                        'Tests/animation_test.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
