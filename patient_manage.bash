
study=$1
echo $study


if [ -e study ]
then
    echo "  *** WARNING : Study Exists *** "
else
    echo "*** Creating study *** : " $study
    mkdir $study
    mkdir -p $study/images
    mkdir -p $study/mlc
    mkdir -p $study/dicom
    mkdir -p $study/clinicalConfig

    mv *$study.mhd $study/images && *$study.raw $study/images
    mv *$study.mlc $study/mlc
    mv *$study.tb $study/clinicalConfig

fi 