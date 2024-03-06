#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Sofa
import Sofa.Core
import Sofa.Simulation
import SofaRuntime
import os
import numpy as np

_runAsPythonScript = False

def get1DIdx(RowIdx,ColIdx):
    Idx1D = RowIdx * 8 + ColIdx
    return Idx1D

class Controller(Sofa.Core.Controller):

    def __init__(self, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.RootNode = kwargs['RootNode']

        self.Counter = 0
        self.IterationCounter = 0
        self.DistributionStride = 5
        self.begun = False

        self.ModelNode = self.RootNode.origami
        self.SurfacePressurePressure = self.ModelNode.cavity.pressure

        self.VolumeChange = 0
        self.VolumeIncrement = 30
        self.SideInflationSign = 1

 
    def onKeypressedEvent(self, c):
        increment=50
        key = c['key']
        
        if (key == "+"):
            pressureValue=self.SurfacePressurePressure.value.value[0] + increment
            self.SurfacePressurePressure.value = [pressureValue]

        if (key == "-"):
            pressureValue=self.SurfacePressurePressure.value.value[0] - increment
            self.SurfacePressurePressure.value = [pressureValue]
