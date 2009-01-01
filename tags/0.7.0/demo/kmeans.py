#!/usr/bin/env python

# OpenCV's Python demo
# -- adapted by Minh-Tri Pham to work with ctypes-opencv
from opencv import *
from random import randint
MAX_CLUSTERS=5

if __name__ == "__main__":

    color_tab = [CV_RGB(255,0,0),CV_RGB(0,255,0),CV_RGB(100,100,255),
        CV_RGB(255,0,255),CV_RGB(255,255,0)];
    img = cvCreateImage( cvSize( 500, 500 ), 8, 3 );
    rng = cvRNG(-1);

    cvNamedWindow( "clusters", 1 );
        
    while True:
        cluster_count = randint(2, MAX_CLUSTERS)
        sample_count = randint(1, 1000)
        points = cvCreateMat( sample_count, 1, CV_32FC2 );
        clusters = cvCreateMat( sample_count, 1, CV_32SC1 );
        
        # generate random sample from multigaussian distribution
        for k in range(cluster_count):
            center = CvPoint(cvRandInt(rng)%img.width, cvRandInt(rng)%img.height)
            first = k*sample_count/cluster_count
            last = sample_count
            if k != cluster_count:
                last = (k+1)*sample_count/cluster_count

            if first >= last:
                continue
                
            cvRandArr( rng, cvGetRows(points, None, first, last), CV_RAND_NORMAL,
                       cvScalar(center.x,center.y,0,0),
                       cvScalar(img.width*0.1,img.height*0.1,0,0));
        

        # shuffle samples 
        cvRandShuffle( points, rng )

        cvKMeans2( points, cluster_count, clusters,
                   cvTermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 1.0 ));

        cvZero( img );

        for i in range(sample_count):
            cluster_idx = clusters[i,0]
            pt = points[i,0]
            pt = cvPoint(cvRound(pt[0]), cvRound(pt[1]))
            cvCircle( img, pt, 2, color_tab[cluster_idx], CV_FILLED, CV_AA, 0 );
        

        cvShowImage( "clusters", img );

        key = cvWaitKey(0)
        if( key == '\x1b' or key == 'q' or key == 'Q' ): # 'ESC'
            break;
    
    
    cvDestroyWindow( "clusters" );
