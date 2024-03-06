import Sofa

import os
path = os.path.dirname(os.path.abspath(__file__))+'/mesh/'

def createScene(rootNode):

                rootNode.addObject('RequiredPlugin', pluginName='SoftRobots SoftRobots.Inverse SofaConstraint SofaDeformable SofaEngine SofaImplicitOdeSolver SofaLoader SofaOpenglVisual SofaPreconditioner SofaSimpleFem SofaSparseSolver SofaTopologyMapping')
                rootNode.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')

                rootNode.addObject('FreeMotionAnimationLoop')
                rootNode.addObject('QPInverseProblemSolver', printLog='0')
                rootNode.addObject('DefaultPipeline', verbose="0")
                rootNode.addObject('BruteForceBroadPhase')
                rootNode.addObject('BVHNarrowPhase')
                rootNode.addObject('DefaultContactManager', response="FrictionContact")
                rootNode.addObject('LocalMinDistance', name="Proximity", alarmDistance="0", contactDistance="0")

		#goal
                goal = rootNode.addChild('goal')
                goal.addObject('EulerImplicitSolver', firstOrder=True)
                goal.addObject('CGLinearSolver', iterations='100', tolerance='1e-05', threshold='1e-05')
                goal.addObject('MechanicalObject', name='goalMO', position='0 0 20')
                goal.addObject('SphereCollisionModel', radius='1', group='3')
                goal.addObject('UncoupledConstraintCorrection')

		#origami
                origami = rootNode.addChild('origami')
                origami.addObject('EulerImplicitSolver', name='odesolver' ,firstOrder=False, rayleighStiffness=0.2, rayleighMass=0.2)
                origami.addObject('ShewchukPCGLinearSolver', iterations='15', name='linearsolver', tolerance='1e-5', preconditioners='preconditioner', use_precond=True, update_step='1')
                origami.addObject('MeshVTKLoader', name='loader', filename=path+'origami2.vtk')
                origami.addObject('MeshTopology', src='@loader', name='container')
                # origami.addObject('TetrahedronSetTopologyModifier')
                origami.addObject('MechanicalObject', name='tetras', template='Vec3', showIndices=False, showIndicesScale='4e-5', rx='0', dz='0')
                origami.addObject('UniformMass', totalMass='0.5')
                origami.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio='0.45',  youngModulus='1000')
                origami.addObject('BoxROI', name='boxROI', box=[-20, -20, 0, 20, 20, -5], drawBoxes=True, position="@tetras.rest_position", tetrahedra="@container.tetrahedra")
                origami.addObject('RestShapeSpringsForceField', points='@boxROI.indices', stiffness='1e12')
                origami.addObject('SparseLDLSolver', name='preconditioner', template="CompressedRowSparseMatrixMat3x3d")
                origami.addObject('LinearSolverConstraintCorrection', solverName='preconditioner')

		#origami/effector
                effector = origami.addChild('effector')
                effector.addObject('MechanicalObject', name="effectorPoint", position="0 0 16")
                effector.addObject('PositionEffector', template='Vec3', indices=0, effectorGoal="@../../goal/goalMO.position")
                effector.addObject('BarycentricMapping', mapForces=False, mapMasses=False)

		#origami/cavity
                cavity = origami.addChild('cavity')
                cavity.addObject('MeshSTLLoader', name='loader', filename=path+'core1.stl')
                cavity.addObject('MeshTopology', src='@loader', name='topo')
                cavity.addObject('MechanicalObject', name='cavity')
                cavity.addObject('SurfacePressureActuator', template='Vec3', triangles='@topo.triangles', maxPressure=30, minPressure=-30, drawPressure=True, drawScale=0.02)
                cavity.addObject('BarycentricMapping', name='mapping',  mapForces=False, mapMasses=False)

		#origami/origamiVisu
                origamiVisu = origami.addChild('visu')
                origamiVisu.addObject('MeshObjLoader', filename=path+"origami2.stl", name="loader")
                origamiVisu.addObject('OglModel', src="@loader", template='Vec3', color=[0.7, 0.7, 0.7, 0.5])

                origamiVisu.addObject('BarycentricMapping')

                return rootNode
