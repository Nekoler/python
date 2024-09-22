import vapoursynth

core = vapoursynth.core
if not 'infile' in globals():
	infile=r''
video = core.ffms2.Source(infile,cache=False)
video = core.misc.SCDetect(video)
video = video.resize.Point(format=vapoursynth.RGBS)
video = core.rife.RIFE(video,model=19,factor_num=5,factor_den=2,gpu_id=1,gpu_thread=3,sc=True,skip=True)
video = video.resize.Point(format=vapoursynth.YUV420P10,matrix=vapoursynth.MATRIX_BT2020_CL)
video.set_output()
