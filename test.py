
# # RT PLAN READER

import sys
import dicom

file=sys.argv[1]
plan = dicom.read_file(file)


# ## CREATE A PYTHON DICTIONARY OBJECT WITH USEFUL DATA OF RT PLAN

#Dictonary which will contains all useful data for RTpla
rt_plan_file = {} 

rt_plan_file['Name'] = plan.PatientName
rt_plan_file['ID'] = plan.PatientID
rt_plan_file['Birth'] = plan.PatientBirthDate

#Create a dictionnary for each beam in RT plan dictionnary
rt_plan_file['Beam'] = {}

for beam_ in plan.BeamSequence:
    
    if beam_.TreatmentDeliveryType == 'TREATMENT':
        
            beam_name=beam_.BeamName
            rt_plan_file['Beam'][beam_name] = {}  #Create a dictionnary for each (treatment Beam)
            rt_plan_file['Beam'][beam_name]['RadiationType'] = beam_.RadiationType
            rt_plan_file['Beam'][beam_name]['Energy']=beam_.ControlPointSequence[0].NominalBeamEnergy
            rt_plan_file['Beam'][beam_name]['BeamType']=beam_.BeamType


            xj = beam_.ControlPointSequence[0].BeamLimitingDevicePositionSequence[0].LeafJawPositions
            yj = beam_.ControlPointSequence[0].BeamLimitingDevicePositionSequence[1].LeafJawPositions

            rt_plan_file['Beam'][beam_name]['x_jaw'] = [float(val) for val in xj]
            rt_plan_file['Beam'][beam_name]['y_jaw'] = [float(val) for val in yj]
            
            if rt_plan_file['Beam'][beam_name]['RadiationType'] == 'ELECTRON':
                rt_plan_file['Beam'][beam_name]['applicatorID'] = beam_.ApplicatorSequence[0].ApplicatorID
                rt_plan_file['Beam'][beam_name]['applicatorType'] = beam_.ApplicatorSequence[0].ApplicatorType
            
            
            rt_plan_file['Beam'][beam_name]['ControlPointSequence']={}
            
            if rt_plan_file['Beam'][beam_name]['BeamType'] == 'DYNAMIC':             

                for control_point_sequence_ in beam_.ControlPointSequence:
                                 
                    control_point_index=control_point_sequence_.ControlPointIndex
                    rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]={}
                    
                    if control_point_index == 0:
                        mlcx = control_point_sequence_.BeamLimitingDevicePositionSequence[2].LeafJawPositions
                        rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]['GantryRotationDirection'] = beam_.ControlPointSequence[0].GantryRotationDirection
                    else:
                        mlcx = control_point_sequence_.BeamLimitingDevicePositionSequence[0].LeafJawPositions
                        
                    rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]['MLCx'] = [float(val) for val in mlcx]
                    rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]['GantryAngle'] = round(float(control_point_sequence_.GantryAngle), 3)
                    rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]['CumulativeDoseCoef'] = round(float(control_point_sequence_.ReferencedDoseReferenceSequence[0].CumulativeDoseReferenceCoefficient), 4)
                    
            if rt_plan_file['Beam'][beam_name]['BeamType'] == 'STATIC':
                
                control_point_index=beam_.ControlPointSequence[0].ControlPointIndex
                rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]={}
                rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]['GantryAngle'] = round(float(beam_.ControlPointSequence[0].GantryAngle), 3)
                
                if len(beam_.ControlPointSequence[0].BeamLimitingDevicePositionSequence) > 2:
                
                    mlcx = beam_.ControlPointSequence[0].BeamLimitingDevicePositionSequence[2].LeafJawPositions
                    rt_plan_file['Beam'][beam_name]['ControlPointSequence'][control_point_index]['MLCx'] = [float(val) for val in mlcx]
#print rt_plan_file   
print "rt_plan_file dictionary  -->  Created"


# ## Write RT plan Summary ".txt"

rt_plan_sumup_name="rt_plan_"+ rt_plan_file['ID'] +'.txt'
rt_plan_sumup=open(rt_plan_sumup_name, 'w') 

rt_plan_sumup.write("*********************** RT PLAN SUMARY ******************************"+'\n') 
rt_plan_sumup.write('\n')
rt_plan_sumup.write('\n')

rt_plan_sumup.write("GENERAL INFORMATION :"  + '\n' + '\n')
rt_plan_sumup.write("     PATIENT Name : " + rt_plan_file['Name'] + '\n')                       #Write  patient name
rt_plan_sumup.write("     PATIENT ID : " + rt_plan_file['ID'] + '\n')                    #write patient ID
rt_plan_sumup.write("     PATIENT Birth Date : " + rt_plan_file['ID'] + '\n' + '\n' + '\n')  

rt_plan_sumup.write("TECHNICAL INFORMATION :"  + '\n' + '\n')
rt_plan_sumup.write("     Number of Treatment Beams : " + str(len(rt_plan_file['Beam'])) + '\n' + '\n')

beamsname=rt_plan_file['Beam'].keys()
for beams in beamsname:
    rt_plan_sumup.write("     Beams Name : " + beams + '\n')
    rt_plan_sumup.write("          Beams Type : " + rt_plan_file['Beam'][beams]['BeamType'] + '\n')
    rt_plan_sumup.write("          Radiation Type : " + rt_plan_file['Beam'][beams]['RadiationType'] + '\n')
    rt_plan_sumup.write("          Nominal Energy : " + str(rt_plan_file['Beam'][beams]['Energy']) + '\n')
    rt_plan_sumup.write("          X jaws opening : " + str(rt_plan_file['Beam'][beams]['x_jaw']) + '\n')
    rt_plan_sumup.write("          Y jaws opening : " + str(rt_plan_file['Beam'][beams]['y_jaw']) + '\n')
    
    if rt_plan_file['Beam'][beams]['RadiationType'] =='ELECTRON':
        rt_plan_sumup.write("          Applicator ID : " + rt_plan_file['Beam'][beam_name]['applicatorID'] + '\n')
        rt_plan_sumup.write("          Applicator Type : " + rt_plan_file['Beam'][beam_name]['applicatorType'] + '\n')
        rt_plan_sumup.write("          Insert : " + rt_plan_file['Beam'][beam_name]['insert'] + '\n')
        rt_plan_sumup.write("          Insert : " + rt_plan_file['Beam'][beam_name]['DSP'] + '\n')

            
    if rt_plan_file['Beam'][beams]['BeamType'] =='STATIC':
        
        rt_plan_sumup.write("          Gantry Angle : " + str(rt_plan_file['Beam'][beams]['ControlPointSequence'][0]['GantryAngle']) + '\n')
        
    if rt_plan_file['Beam'][beams]['BeamType'] =='DYNAMIC':
        
        rt_plan_sumup.write("          Control Point index Number : " + str(len(rt_plan_file['Beam'][beams]['ControlPointSequence'])) + '\n')
        rt_plan_sumup.write("          GantryAngleRotation : " + rt_plan_file['Beam'][beams]['ControlPointSequence'][0]['GantryRotationDirection'] + '\n')
    
    
        rt_plan_sumup.write('\n')

rt_plan_sumup.write(  '\n'  + '\n' + '\n' + '\n')
rt_plan_sumup.write("TECHNICAL INFORMATION DETAILED :"  + '\n' + '\n')


if rt_plan_file['Beam'][beams]['BeamType'] =='DYNAMIC':
    for beams in beamsname:
        rt_plan_sumup.write(" ===== Beams Name : " + beams + ' ======\n' + '\n')

        n_cpi=rt_plan_file['Beam'][beams]['ControlPointSequence'].keys()
        for cpi in n_cpi:
            rt_plan_sumup.write("   *** Control Point Index : " + str(cpi) + ' \n')
            rt_plan_sumup.write("      -> MLCx : " + str(rt_plan_file['Beam'][beams]['ControlPointSequence'][cpi]['MLCx']) + ' \n')
            rt_plan_sumup.write("      -> Gantry Angle : " + str(rt_plan_file['Beam'][beams]['ControlPointSequence'][cpi]['GantryAngle']) + ' \n')
            if 'CumulativeDoseCoef' in rt_plan_file.keys():
                rt_plan_sumup.write("      -> Cumul Dose Coeff : " + str(rt_plan_file['Beam'][beams]['ControlPointSequence'][cpi]['CumulativeDoseCoef']) + ' \n' + ' \n')
        rt_plan_sumup.write('\n')
    
rt_plan_sumup.write('\n')
rt_plan_sumup.close()
print "rt_plan_"+ rt_plan_file['ID'] +'.txt' '  -->'  '  Created' 


# ## Create Clinic_Config.tb rt plan based
# #### one file per beam

# In[20]:


for beams_ in rt_plan_file['Beam'].keys():

    with open('clinic_config_temp.tb', 'r') as file:                                  #laod Config.tb   # Write JAW position in Config.tb file # At the moment only lfor the first Beam
        lines = file.readlines()
         
        x1_val = int(rt_plan_file['Beam'][beams_]['x_jaw'][0])
        x2_val = int(rt_plan_file['Beam'][beams_]['x_jaw'][1])
        y1_val = int(rt_plan_file['Beam'][beams_]['y_jaw'][0])
        y2_val = int(rt_plan_file['Beam'][beams_]['y_jaw'][1])
        
        if x1_val < 0:
            x1_val=int(x1_val*-1)
        if x2_val < 0:
            x2_val=int(x2_val*-1)
        if y1_val < 0:
            y1_val=int(y1_val*-1)
        if y2_val < 0:
            y2_val=int(y2_val*-1)
                
        lines[lines.index("=X1=\n")+1] = str(x1_val) +'\n'
        lines[lines.index("=X2=\n")+1] = str(x2_val) +'\n'
        lines[lines.index("=Y1=\n")+1] = str(y1_val) +'\n'
        lines[lines.index("=Y2=\n")+1] = str(y2_val) +'\n'
        
        if 'MLCx' in rt_plan_file['Beam'][beams_]['ControlPointSequence'][0]:
            
            if rt_plan_file['Beam'][beam_name]['BeamType'] == 'DYNAMIC':        
                lines[lines.index("=MLC=\n")+1] = '2' +'\n'
            if rt_plan_file['Beam'][beam_name]['BeamType'] == 'STATIC' :
                lines[lines.index("=MLC=\n")+1] = '1' +'\n'
        else:
            lines[lines.index("=MLC=\n")+1] = '0' +'\n'
            
        if rt_plan_file['Beam'][beam_name]['BeamType'] == 'STATIC' :
                lines[lines.index("=GANTRY_STOP=\n")+1] = 'X' +'\n'
                lines[lines.index("=GANTRY=\n")+1] = str(rt_plan_file['Beam'][beams_]['ControlPointSequence'][0]['GantryAngle']) +'\n'
        
        if rt_plan_file['Beam'][beam_name]['BeamType'] == 'DYNAMIC' :
            lines[lines.index("=GANTRY_STOP=\n")+1] = str(rt_plan_file['Beam'][beams_]['ControlPointSequence'][len(rt_plan_file['Beam'][beams_]['ControlPointSequence'])-1]['GantryAngle']) +'\n'
            lines[lines.index("=GANTRY=\n")+1] = str(rt_plan_file['Beam'][beams_]['ControlPointSequence'][0]['GantryAngle']) +'\n'
        
            if rt_plan_file['Beam'][beams_]['ControlPointSequence'][0]['GantryRotationDirection'] == 'CW':
                lines[lines.index("=ROTATION_DIRECTION=\n")+1] = '0' +'\n'
            else:
                lines[lines.index("=ROTATION_DIRECTION=\n")+1] = '1' +'\n'
            
        lines[lines.index("=MLC_FILE=\n")+1]='XXX' +'\n'
        
        lines[lines.index("=PHANTOM=\n")+1]='0' +'\n'
        
        lines[lines.index("=ACTOR=\n")+1]='XXX' +'\n'
        
        if rt_plan_file['Beam'][beams_]['RadiationType'] == 'ELECTRON':
            a='E'
        if rt_plan_file['Beam'][beams_]['RadiationType'] == 'PHOTON':
            a='X'
        
        lines[lines.index("=ENERGY=\n")+1]= str(rt_plan_file['Beam'][beams_]['Energy']) + a +'\n'
        
        if rt_plan_file['Beam'][beams_]['RadiationType'] == 'ELECTRON':
            lines[lines.index("=APPLICATOR=\n")+1] = rt_plan_file['Beam'][beams_]['applicatorID'] +'\n'
            lines[lines.index("=INSERT=\n")+1] = rt_plan_file['Beam'][beams_]['applicatorType'].replace('ELECTRON_', '') +'\n'
        
        lines[lines.index("=JOB_NAME=\n")+1] = beams_
        
    with open('ClinicConfig_' + beams_ +'.tb', 'w') as file:                                                                                                      #Write Config.tb with changes
        file.writelines(lines)
    print 'ClinicConfig_'+ beams_ + '.tb' ' -->'  '  Created'  


# ## Create mlc file for GATE

if 'MLCx' in rt_plan_file['Beam'][beams_]['ControlPointSequence'][0]:
    i=1
    for beams_ in rt_plan_file['Beam'].keys():    
        if 'MLCx' in rt_plan_file['Beam'][beams_]['ControlPointSequence'][0]:

            if rt_plan_file['Beam'][beams_]['BeamType'] == 'DYNAMIC':
                mlc_file = open('dynamicMLC_'+ beams_ + '.mlc', 'w')

            if rt_plan_file['Beam'][beams_]['BeamType'] == 'STATIC':
                mlc_file = open('staticMLC_' + beams_ + '.mlc', 'w')

            mlc_file.write('File Rev = H ' + '\n')
            mlc_file.write('Treatment = ' + rt_plan_file['Beam'][beams_]['BeamType'] + '\n')
            mlc_file.write('Last Name = ' + rt_plan_file['Name'] + '\n')
            mlc_file.write('First Name = ' + '\n')
            mlc_file.write('Patient ID = ' + rt_plan_file['ID'] + '\n')
            mlc_file.write('Number of Fields = ' + str(len(rt_plan_file['Beam'][beams_]['ControlPointSequence'])) + '\n')
            mlc_file.write('Model = Varian HD120' + '\n')
            mlc_file.write('Tolerance = 0.00' + '\n')
            mlc_file.write('\n')

            j=0
            for cpi in rt_plan_file['Beam'][beams_]['ControlPointSequence']:


                mlc_file.write('Field = ' + 'Beam ' + str(i)+'.'+str(j) + '\n')
                if rt_plan_file['Beam'][beams_]['BeamType'] == 'STATIC':
                    mlc_file.write('Index = ' + str(rt_plan_file['Beam'][beams_]['ControlPointSequence'][cpi]['GantryAngle']) + '\n')
                if rt_plan_file['Beam'][beams_]['BeamType'] == 'DYNAMIC':
                    mlc_file.write('Index = ' + str(rt_plan_file['Beam'][beams_]['ControlPointSequence'][cpi]['GantryAngle']) + '\n')            

                mlc_file.write('Carriage Group = 1 ' + '\n')
                mlc_file.write('Operator = ' + '\n')
                mlc_file.write('Collimator = 0.00' + '\n')  

                ii=0
                for leafs_ in rt_plan_file['Beam'][beams_]['ControlPointSequence'][cpi]['MLCx']:

                    if ii < 60:
                        mlc_file.write('Leaf ' + str(ii + 1) + 'A = ' + str(leafs_) + '\n')
                    else:
                        mlc_file.write('Leaf ' + str(ii - 59) + 'B = ' + str(leafs_) + '\n')

                    ii=ii+1

                mlc_file.write('Note = 0' + '\n')
                mlc_file.write('Shape = 0' + '\n')
                mlc_file.write('Magnification  = 1.00' + '\n' + '\n')            
                j=j+1            
        i=i+1            
    mlc_file.close()
else:
    print('No mlc in this beam plan')

