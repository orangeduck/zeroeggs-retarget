import os

def select_branch(node):
    if isinstance(node, pyfbsdk.FBModel):
        
        node.Selected = True
        
        for child in node.Children:
            select_branch(child)

def find_nubs(out, node):
    if isinstance(node, pyfbsdk.FBModel):
        
        if str(node.Name).endswith('_End'):
            out.append(node)
        
        for child in node.Children:
            find_nubs(out, child)

def deselect_all():
    selected_models = FBModelList()
    FBGetSelectedModels(selected_models, None, True)
    for select in selected_models:
        select.Selected = False;

data_path = 'C:/Dev/ubisoft-laforge-ZeroEGGS/data/clean'
out_path = 'C:/Dev/zeroeggs-retarget/fbx'

bvh_files = [f for f in os.listdir(data_path) if f.endswith('.bvh')]


for file in bvh_files:
    
    bvh_file = os.path.join(data_path, file)
    fbx_file = os.path.join(out_path, file.replace('.bvh', '.fbx'))

    print('Creating %s' % fbx_file)
    
    FBApplication().FileOpen('C:/Dev/zeroeggs-retarget/Geno.fbx')
    FBSystem().Scene.Characters[0].FBDelete()
    FBApplication().FileImport(bvh_file, True)
    
    nubs = []
    find_nubs(nubs, FBFindModelByLabelName('Hips'))
    for nub in nubs:
            nub.FBDelete()
    
    deselect_all()
    select_branch(FBFindModelByLabelName('Hips'))
    
    print('Translating Down Vertically')

    hip_node = FBFindModelByLabelName('Hips')
    curve = hip_node.Translation.GetAnimationNode().Nodes[1].FCurve
    
    for i in range(len(curve.Keys)):
        curve.KeySetValue(i, curve.KeyGetValue(i) - 2.25)
    
    FBFindModelByLabelName('Geno').Selected = True
    
    save_options = FBFbxOptions(False)
    save_options.SaveSelectedModelsOnly = True
    
    print('Saving FBX...')
    
    FBApplication().FileSave(fbx_file, save_options)
    
    # break