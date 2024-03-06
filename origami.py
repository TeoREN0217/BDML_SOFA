# -*- coding: utf-8 -*-

import Sofa.Core
import Sofa.Simulation
import SofaRuntime
import sys
import numpy as np
import os
from Controller import Controller
path = os.path.dirname(os.path.abspath(__file__)) + '/mesh/'


def createScene(rootNode):
    rootNode.addObject('RequiredPlugin', name='SoftRobots')
    rootNode.addObject('RequiredPlugin', name='SofaPython3')
    rootNode.addObject('RequiredPlugin', pluginName=[
        "Sofa.Component.AnimationLoop",  # Needed to use components FreeMotionAnimationLoop
        "Sofa.Component.Constraint.Lagrangian.Correction",
        # Needed to use components LinearSolverConstraintCorrection
        "Sofa.Component.Constraint.Lagrangian.Solver",  # Needed to use components GenericConstraintSolver
        "Sofa.Component.Engine.Select",  # Needed to use components BoxROI
        "Sofa.Component.IO.Mesh",  # Needed to use components MeshSTLLoader, MeshVTKLoader
        "Sofa.Component.LinearSolver.Direct",  # Needed to use components SparseLDLSolver
        "Sofa.Component.Mass",  # Needed to use components UniformMass
        "Sofa.Component.ODESolver.Backward",  # Needed to use components EulerImplicitSolver
        "Sofa.Component.Setting",  # Needed to use components BackgroundSetting
        "Sofa.Component.SolidMechanics.FEM.Elastic",  # Needed to use components TetrahedronFEMForceField
        "Sofa.Component.SolidMechanics.Spring",  # Needed to use components RestShapeSpringsForceField
        "Sofa.Component.Topology.Container.Constant",  # Needed to use components MeshTopology
        "Sofa.Component.Visual",  # Needed to use components VisualStyle
        "Sofa.GL.Component.Rendering3D",  # Needed to use components OglModel
    ])
    rootNode.addObject('VisualStyle', displayFlags="showVisualModels hideBehaviorModels hideCollisionModels \
                        hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe")

    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')

    rootNode.addObject('GenericConstraintSolver', maxIterations=1000, tolerance=1e-3)

    rootNode.addObject('BackgroundSetting')
    rootNode.findData('gravity').value = [0, 0, -981.0]
    rootNode.findData('dt').value = 0.01

    ##########################################
    # FEM Model                              #
    ##########################################
    origami = rootNode.addChild('origami')
    origami.addObject('EulerImplicitSolver', firstOrder=False, rayleighStiffness=0.2, rayleighMass=0.2)
    origami.addObject('SparseLDLSolver')

    origami.addObject('MeshVTKLoader', name='loader', filename=path + 'origami2.vtk', rotation=[0, 0, 0])
    origami.addObject('MeshTopology', src='@loader')

    origami.addObject('MechanicalObject', name='tetras', template='Vec3')
    origami.addObject('UniformMass', totalMass=0.030)
    origami.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio=0.45, youngModulus=100)

    origami.addObject('BoxROI', name='ROI1', box=[-20, -20, 0, 20, 20, -5], drawBoxes=True)
    origami.addObject('RestShapeSpringsForceField', points='@ROI1.indices', stiffness=1e12)
    # origami.addObject('FixedConstraint', indices='@ROI1.indices')

    origami.addObject('LinearSolverConstraintCorrection')

    ##########################################
    # Pressure                               #
    ##########################################
    #  This add a new node in the scene. This node is appended to the origami's node.
    cavity = origami.addChild('cavity')

    #  This adds a MechanicalObject, a component holding the degree of freedom of our
    # mechanical modelling. In the case of a pneumatic actuation it is a set of positions describing the cavity wall.
    cavity.addObject('MeshSTLLoader', name='loader', filename=path + 'core1.stl')
    cavity.addObject('MeshTopology', src='@loader', name='topo')
    cavity.addObject('MechanicalObject', name='cavity')

    # Add a SurfacePressureConstraint object with a name.
    cavity.addObject('SurfacePressureConstraint', template='Vec3', name="pressure",triangles='@topo.triangles', valueType=1, value=0)
    # This adds a BarycentricMapping. A BarycentricMapping is a key element as it will add a bi-directional link
    #  between the cavity wall (surfacic mesh) and the origami (volumetric mesh) so that movements of the cavity's DoFs will be mapped
    #  to the origami and vice-versa;
    cavity.addObject('BarycentricMapping', name='mapping', mapForces=False, mapMasses=False)

    ##########################################
    # Visualization                          #
    ##########################################
    origamiVisu = origami.addChild('visu')
    origamiVisu.addObject('MeshSTLLoader', filename=path + "origami2.stl", name="loader")
    origamiVisu.addObject('OglModel', src="@loader", color=[0.4, 0.4, 0.4, 0.5])
    origamiVisu.addObject('BarycentricMapping')

    rootNode.addObject(Controller(name="Controller", RootNode=rootNode))
    
    return rootNode
