import unittest


class shiftPlanner:
    def __init__(self, numberOfB6, numberOfB5, numberOfHCA):
        self.numberOfB6 = numberOfB6
        self.numberOfB5 = numberOfB5
        self.numberOfHCA = numberOfHCA
        self.rota = []
        self.GetEmptyRota()

    def GetShifts(self, numberOfFourWeekBlocks):
        shifts = []
        for day in range(28 * numberOfFourWeekBlocks):
            shifts.append('LD')
            shifts.append('N')
        return shifts

    def GetEmptyRota(self):
        nurseNumber = 1
        for B6 in range(self.numberOfB6):
            nurse = Nurse(str(nurseNumber), 'B6', [])
            self.rota.append(nurse)
            nurseNumber += 1

        for B5 in range(self.numberOfB5):
            nurse = Nurse(str(nurseNumber), 'B5', [])
            self.rota.append(nurse)
            nurseNumber += 1
        for HCA in range(self.numberOfHCA):
            nurse = Nurse(str(nurseNumber), 'HCA', [])
            self.rota.append(nurse)
            nurseNumber += 1

    def AddShiftToNurse(self, name, shift):
        for nurse in self.rota:
            if nurse.name == name:
                nurse.shifts.append(shift)


class Nurse:
    def __init__(self, name, rank, shifts):
        self.name = name
        self.rank = rank
        self.shifts = shifts


class Shift:
    def __init__(self, shiftType='', day=0):
        self.shiftType = shiftType
        self.day = day


class test_shiftPlanner(unittest.TestCase):
    def setUp(self):
        self.B6 = 4
        self.B5 = 16
        self.HCA = 4
        self.ShiftPlanner = shiftPlanner(self.B6, self.B5, self.HCA)

    def test_oneMonthHas56Shifts(self):
        self.assertEqual(56, len(self.ShiftPlanner.GetShifts(1)))

    def test_rotaHasCorrectNumbersOfEachRank(self):
        numberOfB6 = 0
        numberOfB5 = 0
        numberOfHCA = 0

        for nurse in self.ShiftPlanner.rota:
            if nurse.rank == 'B6':
                numberOfB6 += 1
            elif nurse.rank == 'B5':
                numberOfB5 += 1
            elif nurse.rank == 'HCA':
                numberOfHCA += 1
            else:
                self.assertEqual(0, 1, msg='There is a nurse with an unrecognised rank in the rota.')

        self.assertEqual(self.B6, numberOfB6)
        self.assertEqual(self.B5, numberOfB5)
        self.assertEqual(self.HCA, numberOfHCA)

    def test_correctShiftAddedToNurse(self):
        name = str(1)
        shiftType = 'LD'
        day = 1

        self.ShiftPlanner.AddShiftToNurse(name, Shift(shiftType, day))
        for nurse in self.ShiftPlanner.rota:
            if nurse.name == name:
                self.assertEqual(nurse.shifts[0].shiftType, Shift(shiftType, day).shiftType)
                self.assertEqual(nurse.shifts[0].day, Shift(shiftType, day).day)
