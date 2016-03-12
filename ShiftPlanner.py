import unittest
import numpy as np
import cv2

boxSize = 60
blankRotaImage = np.zeros((boxSize * 4, boxSize * 7, 3))
for x in xrange(1, 7):
    x *= boxSize
    blankRotaImage[:, x] = 255
for y in xrange(1, 4):
    y *= boxSize
    blankRotaImage[y, :] = 255

rotaImagePositionDict = {'1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (0, 3), '5': (0, 4), '6': (0, 5), '7': (0, 6),
                         '8': (1, 0), '9': (1, 1), }

class shiftPlanner:
    def __init__(self, numberOfB6, numberOfB5, numberOfHCA, months):
        self.numberOfB6 = numberOfB6
        self.numberOfB5 = numberOfB5
        self.numberOfHCA = numberOfHCA
        self.rota = Rota(months)
        self.staff = self.GetStaffList()

    def GetStaffList(self):
        staff = []
        nurseNumber = 1
        for i in range(self.numberOfB6):
            staff.append(Nurse(str(nurseNumber), 'B6', []))
            nurseNumber += 1
        for i in range(self.numberOfB5):
            staff.append(Nurse(str(nurseNumber), 'B5', []))
            nurseNumber += 1
        for i in range(self.numberOfHCA):
            staff.append(Nurse(str(nurseNumber), 'HCA', []))
            nurseNumber += 1
        return staff

    def AddNurseToShift(self, nurse, shift):
        shift.nurses.append(nurse)
        nurse.shifts.append(shift)

    def PopulateRota(self):
        iterations = 0
        while iterations < 1000:
            for shift in self.rota.days:
                while shift.GetNumberOfRank('B6') < 1 and iterations < 1000:
                    iterations += 1
                    for nurse in self.staff:
                        if nurse.IsEligibleForShift(shift, 'B6'):
                            self.AddNurseToShift(nurse, shift)
                while shift.GetNumberOfRank('B5') < 4 and iterations < 1000:
                    iterations += 1
                    for nurse in self.staff:
                        if nurse.IsEligibleForShift(shift, 'B5'):
                            self.AddNurseToShift(nurse, shift)
                while shift.GetNumberOfRank('HCA') < 1 and iterations < 1000:
                    iterations += 1
                    for nurse in self.staff:
                        if nurse.IsEligibleForShift(shift, 'HCA'):
                            self.AddNurseToShift(nurse, shift)


class Rota(object):
    def __init__(self, months):
        self.months = months
        self.days = []
        for day in xrange(1, (28 * months) + 1):
            self.days.append(Shift('LD', day))
            self.days.append(Shift('N', day))

    def DisplayRota(self):
        for month in xrange(1, self.months + 1):
            cv2.imshow('Rota for month ' + str(month), blankRotaImage)
        cv2.waitKey(0)


class Shift(object):
    def __init__(self, shiftType, day):
        self.shiftType = shiftType
        self.day = day
        self.nurses = []
        if shiftType == 'LD':
            self.length = 13
        elif shiftType == 'N':
            self.length = 12

    def GetNumberOfRank(self, rank):
        number = 0
        for nurse in self.nurses:
            if nurse.rank == rank:
                number += 1
        return number


class Nurse(object):
    def __init__(self, name, rank, shifts):
        self.name = name
        self.rank = rank
        self.shifts = shifts

    def GetHours(self):
        hours = 0
        for shift in self.shifts:
            if shift.shiftType == 'LD':
                hours += 13
            elif shift.shiftType == 'N':
                hours += 12
        return hours

    def IsEligibleForShift(self, shift, rank):
        if self.GetHours() < 150:
            days = []
            for shift in self.shifts:
                days.append(shift.day)
            if shift.day not in days:
                if self.rank == rank:
                    return True
        else:
            return False

    def DisplayRota(self):
        rotaImage = blankRotaImage
        for shift in self.shifts:
            row, col = 0, 0
            for i in xrange(1, shift.day):
                if i % 7.0 == 0:
                    col = 0
                    row += 1
                col += 1
            if shift.shiftType == 'LD':
                rotaImage[(row * boxSize) + 1:(row * boxSize) + boxSize, (col * boxSize) + 1:(col * boxSize) + boxSize] += (0, 0, 255)
            if shift.shiftType == 'N':
                rotaImage[(row * boxSize) + 1:(row * boxSize) + boxSize, (col * boxSize) + 1:(col * boxSize) + boxSize] += (255, 0, 0)
        cv2.imshow('Rota for ' + self.name, rotaImage)
        cv2.waitKey(0)


class test_shiftPlanner(unittest.TestCase):
    def setUp(self):
        self.B6 = 5
        self.B5 = 19
        self.HCA = 5
        self.months = 1
        self.ShiftPlanner = shiftPlanner(self.B6, self.B5, self.HCA, self.months)

    # def test_addNurseToShift(self):
    #     nurse = Nurse('1', 'B6', [])
    #     self.ShiftPlanner.AddNurseToShift(nurse, self.ShiftPlanner.rota.days[0])
    #     self.assertEqual(self.ShiftPlanner.rota.days[0].nurses[0], nurse)

    def test_showShifts(self):
        self.ShiftPlanner.PopulateRota()
        for staff in self.ShiftPlanner.rota.days:
            for nurse in staff.nurses:
                print nurse.name, ' has ', len(nurse.shifts), ' shift/s this month.'