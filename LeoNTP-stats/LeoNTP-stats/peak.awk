# save all the images with peaks higher than 20k/sec

{ 
	if ($2 > maxval){
		maxval = 1 * $2
		maxtime = $1
		gsub(":", "", maxtime)
	}
}

END{
	if (maxval > 20000){
		HSIZE = 1160
		print maxtime, maxval
		system("rrdtool graph --start " maxtime-HSIZE/2-1 " --end " maxtime+HSIZE/2 " --width " HSIZE " --height 250 --lower-limit 0 --font DEFAULT:0:Helvetica " maxtime "-" maxval ".png DEF:req=ntp1.rrd:req:AVERAGE VDEF:reqmax=req,MAXIMUM LINE1:req#FF0000 LINE1:reqmax#E0E0FF")

	}
}


