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
        for shift in self.rota.days:
            B5s = shift.GetNumberOfRank('B5')
            B6s = shift.GetNumberOfRank('B6')
            HCAs = shift.GetNumberOfRank('HCA')
            while B6s < 1:
                for nurse in self.staff:
                    if nurse.IsEligibleForShift(shift, 'B6'):
                        self.AddNurseToShift(nurse, shift)
                        B6s += 1
                        break
            while B5s < 4:
                for nurse in self.staff:
                    if nurse.IsEligibleForShift(shift, 'B5'):
                        self.AddNurseToShift(nurse, shift)
                        B5s += 1
                        break
            while HCAs < 1:
                for nurse in self.staff:
                    if nurse.IsEligibleForShift(shift, 'HCA'):
                        self.AddNurseToShift(nurse, shift)
                        HCAs += 1
                        break
            print shift.day, B6s, B5s, HCAs


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
            if shift.shiftType == 'N':
                hours += 12
        return hours

    def IsEligibleForShift(self, shift, rank):
        if self.GetHours() < 150:
            days = []
            for workedShift in self.shifts:
                days.append(workedShift.day)
            if shift.day not in days:
                if self.rank == rank:
                    return True
        else:
            return False

    def DisplayRota(self):
        rotaImage = np.zeros((boxSize * 4, boxSize * 7, 3))
        for x in xrange(1, 7):
            x *= boxSize
            blankRotaImage[:, x] = 255
        for y in xrange(1, 4):
            y *= boxSize
            rotaImage[y, :] = 255
        for shift in self.shifts:
            row, col = 0, 0
            for i in xrange(1, shift.day):
                if i % 7.0 == 0:
                    col = 0
                    row += 1
                else:
                    col += 1
            if shift.shiftType == 'LD':
                rotaImage[(row * boxSize) + 1:(row * boxSize) + boxSize, (col * boxSize) + 1:(col * boxSize) + boxSize] += (0, 0, 255)
            if shift.shiftType == 'N':
                rotaImage[(row * boxSize) + 1:(row * boxSize) + boxSize, (col * boxSize) + 1:(col * boxSize) + boxSize] += (255, 0, 0)
        cv2.imshow('Rota for ' + self.name, rotaImage)
        cv2.waitKey(0)


class test_shiftPlanner(unittest.TestCase):
    def setUp(self):
        self.B6 = 6
        self.B5 = 25
        self.HCA = 6
        self.months = 1
        self.ShiftPlanner = shiftPlanner(self.B6, self.B5, self.HCA, self.months)

    def test_showShifts(self):
        self.ShiftPlanner.PopulateRota()
        for nurse in self.ShiftPlanner.staff:
            print nurse.GetHours()
            nurse.DisplayRota()
            cv2.destroyAllWindows()
