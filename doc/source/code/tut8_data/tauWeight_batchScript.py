ó
®ëYc           @   sÎ   d  Z  d d l Z d d l m Z m Z d d l m Z d d l m Z d d l Z d d l	 m
 Z
 d d l m Z e j   Z e j   d k r¢ e j d  n  d	   Z d
   Z d e f d     YZ d S(   s[   
batch.py 

Class to setup and run batch simulations

Contributors: salvadordura@gmail.com
iÿÿÿÿN(   t   izipt   product(   t   popen2(   t   sleep(   t   specs(   t   hi    c         C   st   d d l  m } m } d Gt j   GHd |  | | f } | d GH| | j d  d | d | } | j j   GHd  S(	   Niÿÿÿÿ(   t   Popent   PIPEs   
Job in rank id: s"   nrniv %s simConfig=%s netParams=%ss   
t    t   stdoutt   stderr(   t
   subprocessR   R   t   pct   idt   splitR	   t   read(   t   scriptt   cfgSavePatht   netParamsSavePathR   R   t   commandt   proc(    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyt   runJob   s    	!c         C   sÔ   t  |   t k rK x» |  D]+ } t  |  t t g k r t |  q q Wn t  |   t k rÐ xp |  j   D]_ \ } } t  |  t t g k r t |  n  t  |  t k rj |  j |  |  t |  <qj qj Wn  |  S(   N(   t   typet   listt   dictt
   tupleToStrt	   iteritemst   tuplet   popt   str(   t   objt   itemt   keyt   val(    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyR      s    #t   Batchc           B   s;   e  Z d  d d d i  d  Z d   Z d   Z d   Z RS(   s   cfg.pys   netParams.pyc   	      C   sä   d t  t j j    |  _ | |  _ | |  _ | |  _ d |  j |  _ d |  _	 i  |  _
 g  |  _ | r¦ x; | j   D]* \ } } |  j j i | d 6| d 6 qu Wn  | rà x1 |  j D]# } | d | k r¶ t | d <q¶ q¶ Wn  d  S(   Nt   batch_t   /t   gridt   labelt   valuest   group(   R   t   datetimet   datet   todayt
   batchLabelt   cfgFilet   initCfgt   netParamsFilet
   saveFoldert   methodt   runCfgt   paramsR   t   appendt   True(	   t   selfR-   R/   R3   t   groupedParamsR.   t   kt   vt   p(    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyt   __init__1   s    						% c         C   s  d d  l  } d d l m } | j j |  } | j |  d } | j d  d } y | j |  Wn/ t k
 r | j j |  s d G| GHq n X| |  j	  } i t
 |  d 6} | d k rd d  l }	 d	 | GHt | d
  # }
 |	 j | |
 d d d t Wd  QXn  d  S(   Niÿÿÿÿ(   t   deepcopyi    t   .i   s    Could not createt   batcht   jsons   Saving batch to %s ... t   wt   indenti   t	   sort_keys(   t   ost   copyR<   t   patht   basenameR   t   mkdirt   OSErrort   existst   __dict__R   R?   t   opent   dumpR5   (   R6   t   filenameRC   R<   RF   t   foldert   extt   odictt   dataSaveR?   t   fileObj(    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyt   saveA   s"    	c         C   s   t  | t  r |  j } xT t t |  d  D]< } t  | t j  r] t | | |  } q/ | | | } q/ W| | | d <n t |  j | |  d  S(   Ni   iÿÿÿÿ(	   t
   isinstanceR   t   cfgt   ranget   lenR   t	   SimConfigt   getattrt   setattr(   R6   t
   paramLabelt   paramValt	   containert   ip(    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyt   setCfgNestedParamZ   s    	c   4      C   sQ	  |  j  d> k rM	d d  l } d d  l } y | j |  j  Wn5 t k
 rr | j j |  j  ss d G|  j GHqs n X|  j d |  j d } |  j	 |  |  j d |  j d } | j
 d | j j t  d	 |  |  j d |  j d
 } | j
 d |  j d	 |  | j j |  j  j d  d } t j | |  j  } | j |  _ t |  j _ t |  j  d k r x0 |  j j   D] \ } } |  j | |  q}Wn  |  j  d k rt }	 t }
 xI |  j D]> } d | k rêt | d <t }
 qÅ| d t k rÅt }	 qÅqÅW|
 rVt g  |  j D]* } | d t k r| d | d f ^ q  \ } } n d? } d@ } t g  |  j D]* } | d t k ro| d | d f ^ qo  \ } } t t |    } t t g  | D] } t t |   ^ qÇ   } |	 r{t g  |  j D]* } | d t k rþ| d | d f ^ qþ  \ } } t  |   } t  g  | D] } t t |   ^ qM  } | | } qdA g } dB g } n  |  j! j" d d   d k rÛx- t t$ t% j&     D] } t% j'   qÄWn  x7t | |  D]&\ } } xt | |  D]\ } } |	 r0| | } | | } n | } | } | G| GHxM t( |  D]? \ } } | | } |  j | |  t) |  d t) |  GHqRW|  j d j* g  | D] } d j* d t) |   ^ q¨ } |  j d | } |  j! j" d t  r| j | d  rd | GHní|  j! j" d t  rJ| j | d  rJd | GHn¹|  j! j" d d   r| j | |  j! d  rd | |  j! d f GHnq| |  j _+ |  j |  j _ |  j d | d } |  j j	 |  |  j! j" d d   d k r|  j! j" d d  }  t, |   |  j! j" d  d  }! |  j! j" d! d  }" |  j! j" d" d#  }# |  j! j" d$ d%  }$ |  j! j" d& d'  }% |  j! j" d( d)  }& d* |! |" f }' |! |" }( d+ |$ |( |# | | f }) t- d,  \ }* }+ d- | |% |& |' | | |) f }, |+ j. |,  |, d. GH|+ j/   nò|  j! j" d d   d/ k r¦|  j! j" d d  }  t, |   |  j! j" d0 d1  }- |  j! j" d  d  }! |  j! j" d2 d  }. |  j! j" d3 d4  }/ |  j! j" d5 d  }0 |  j! j" d" d#  }# |  j! j" d$ d6  }$ |  j! j" d& d'  }% |! |. }( d+ |$ |( |# | | f }) d7 | |- |% |! |. | | |/ |0 |) f
 }, d8 G| GH|, d. GHd9 | }1 t0 |1 d:   }2 |2 j. d; |,  Wd  QXt- d< |1  \ }* }3 |3 j/   n] |  j! j" d d   d k r	|  j d | } d8 G| GHt% j1 t2 |  j! j" d" d#  | |  n  t, d  qWqëWy! x t% j3   r4	t, d  q	WWn n Xt, d=  n  d  S(C   NR%   R   iÿÿÿÿs    Could not createR$   s   _batch.jsons   _batchScript.pys   cp R   s   _netParams.pyR=   i    R(   R&   R'   R   t   mpis    = t    t   _t   skips   .jsons3   Skipping job %s since output file already exists...t   skipCfgs	   _cfg.jsons0   Skipping job %s since cfg file already exists...t
   skipCustoms/   Skipping job %s since %s file already exists...t
   hpc_torquet   sleepIntervali   t   nodest   ppnR   s   init.pyt
   mpiCommandt   mpiexect   walltimes   00:30:00t	   queueNamet   defaults   nodes=%d:ppn=%ds9   %s -np %d nrniv -python -mpi %s simConfig=%s netParams=%st   qsubs  #!/bin/bash 
                            #PBS -N %s
                            #PBS -l walltime=%s
                            #PBS -q %s
                            #PBS -l %s
                            #PBS -o %s.run
                            #PBS -e %s.err
                            cd $PBS_O_WORKDIR
                            echo $PBS_O_WORKDIR
                            %ss   
t	   hpc_slurmt
   allocationt   csd403t   coresPerNodet   emails   a@b.cRN   t   ibrunsþ   #!/bin/bash 
#SBATCH --job-name=%s
#SBATCH -A %s
#SBATCH -t %s
#SBATCH --nodes=%d
#SBATCH --ntasks-per-node=%d
#SBATCH -o %s.run
#SBATCH -e %s.err
#SBATCH --mail-user=%s
#SBATCH --mail-type=end

source ~/.bashrc
cd %s
%s
wait
                            s   Submitting job s	   %s.sbatchR@   s   %ss   sbatch i
   (   R%   R   (    (    (   i    (   i    (4   R1   RC   t   globRG   R0   RH   RE   RI   R,   RS   t   systemt   realpatht   __file__R/   RF   R-   R   t   impt   load_sourceRU   t   Falset   checkErrorsRW   R.   R   R_   R3   R5   t   zipR   R   RV   R    R2   t   gett   Nonet   intR   t   nhostt	   runworkert	   enumerateR   t   joint   simLabelR   R   t   writet   closeRK   t   submitR   t   working(4   R6   RC   Rv   t
   targetFileR   t   cfgModuleNamet	   cfgModuleR[   R\   R7   t   ungroupedParamsR:   t	   labelListt
   valuesListt   valueCombinationst   xt   indexCombinationst   labelListGroupt   valuesListGroupt   valueCombGroupst   indexCombGroupst   iworkert   iCombGt   pCombGt   iCombNGt   pCombNGt   iCombt   pCombt   iR   t   jobNameR   Rg   Rh   Ri   R   Rj   Rl   Rm   t   nodesppnt   numprocR   t   outputt   inputt	   jobStringRq   Rs   Rt   RN   t	   batchfilet	   text_filet   pinput(    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyt   runf   sî    %"
	IF1F+	
	
<((/

	

(		
	(N(   t   __name__t
   __module__R   R;   RS   R_   R©   (    (    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyR"   /   s   		(   t   __doc__R)   t	   itertoolsR    R   R   t   timeR   Rz   t   netpyneR   t   neuronR   t   ParallelContextR   R   t   master_works_on_jobsR   R   t   objectR"   (    (    (    s?   /u/salvadord/Documents/ISB/Models/netpyne_repo/netpyne/batch.pyt   <module>   s    			