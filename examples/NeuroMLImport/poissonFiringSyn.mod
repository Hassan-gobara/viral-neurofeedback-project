TITLE Mod file for component: Component(id=poissonFiringSyn type=poissonFiringSynapse)

COMMENT

    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.5.3
         org.neuroml.model   v1.5.3
         jLEMS               v0.9.9.0

ENDCOMMENT

NEURON {
    POINT_PROCESS poissonFiringSyn
    ELECTRODE_CURRENT i
    RANGE averageRate                       : parameter
    RANGE averageIsi                        : parameter
    
    RANGE i                                 : exposure
    RANGE syn0_tauRise                      : parameter
    RANGE syn0_tauDecay                     : parameter
    RANGE syn0_peakTime                     : parameter
    RANGE syn0_waveformFactor               : parameter
    RANGE syn0_gbase                        : parameter
    RANGE syn0_erev                         : parameter
    
    RANGE syn0_g                            : exposure
    
    RANGE syn0_i                            : exposure
    : Based on netstim.mod
    THREADSAFE : only true if every instance has its own distinct Random
    POINTER donotuse
}

UNITS {
    
    (nA) = (nanoamp)
    (uA) = (microamp)
    (mA) = (milliamp)
    (A) = (amp)
    (mV) = (millivolt)
    (mS) = (millisiemens)
    (uS) = (microsiemens)
    (molar) = (1/liter)
    (kHz) = (kilohertz)
    (mM) = (millimolar)
    (um) = (micrometer)
    (umol) = (micromole)
    (S) = (siemens)
    
}

PARAMETER {
    
    averageRate = 0.05 (kHz)
    averageIsi = 20 (ms)
    syn0_tauRise = 0.5 (ms)
    syn0_tauDecay = 10 (ms)
    syn0_peakTime = 1.5767012 (ms)
    syn0_waveformFactor = 1.2324 
    syn0_gbase = 0.002 (uS)
    syn0_erev = 0 (mV)
}

ASSIGNED {
    v (mV)
    
    syn0_g (uS)                            : derived variable
    
    syn0_i (nA)                            : derived variable
    
    i (nA)                                 : derived variable
    rate_tsince (ms/ms)
    rate_syn0_A (/ms)
    rate_syn0_B (/ms)
    donotuse
}

STATE {
    tsince (ms) 
    isi (ms) 
    syn0_A  
    syn0_B  
    
}

INITIAL {
    rates()
    rates() ? To ensure correct initialisation.
    
    tsince = 0
    
    isi = -  averageIsi  * log(1 - random_float(1))
    
    net_send(0, 1) : go to NET_RECEIVE block, flag 1, for initial state
    
    syn0_A = 0
    
    syn0_B = 0
    
}

BREAKPOINT {
    
    SOLVE states METHOD cnexp
    
    
}

NET_RECEIVE(flag) {
    
    LOCAL weight
    
    
    if (flag == 1) { : Setting watch for top level OnCondition...
        WATCH (tsince  >  isi) 1000
    }
    if (flag == 1000) {
    
        tsince = 0
    
        isi = -  averageIsi  * log(1 - random_float(1))
    
        : Child: Component(id=syn0 type=expTwoSynapse)
    
        : This child is a synapse; defining weight
        weight = 1
    
        : paramMappings are: {poissonFiringSyn={tsince=tsince, isi=isi, averageRate=averageRate, averageIsi=averageIsi, i=i}, syn0={A=syn0_A, B=syn0_B, tauRise=syn0_tauRise, tauDecay=syn0_tauDecay, peakTime=syn0_peakTime, waveformFactor=syn0_waveformFactor, gbase=syn0_gbase, erev=syn0_erev, g=syn0_g, i=syn0_i}}
        : state_discontinuity(syn0_A, syn0_A  + (weight *  syn0_waveformFactor ))
        syn0_A = syn0_A  + (weight *  syn0_waveformFactor )
    
        : paramMappings are: {poissonFiringSyn={tsince=tsince, isi=isi, averageRate=averageRate, averageIsi=averageIsi, i=i}, syn0={A=syn0_A, B=syn0_B, tauRise=syn0_tauRise, tauDecay=syn0_tauDecay, peakTime=syn0_peakTime, waveformFactor=syn0_waveformFactor, gbase=syn0_gbase, erev=syn0_erev, g=syn0_g, i=syn0_i}}
        : state_discontinuity(syn0_B, syn0_B  + (weight *  syn0_waveformFactor ))
        syn0_B = syn0_B  + (weight *  syn0_waveformFactor )
    
        net_event(t)
        WATCH (tsince  >  isi) 1000
    
    }
    
}

DERIVATIVE states {
    rates()
    tsince' = rate_tsince 
    syn0_A' = rate_syn0_A 
    syn0_B' = rate_syn0_B 
    
}

PROCEDURE rates() {
    
    syn0_g = syn0_gbase  * ( syn0_B  -  syn0_A ) ? evaluable
    syn0_i = syn0_g  * ( syn0_erev  - v) ? evaluable
    ? DerivedVariable is based on path: synapse/i, on: Component(id=poissonFiringSyn type=poissonFiringSynapse), from synapse; Component(id=syn0 type=expTwoSynapse)
    i = syn0_i ? path based, prefix = 
    
    rate_tsince = 1 ? Note units of all quantities used here need to be consistent!
    
     
    rate_syn0_A = - syn0_A  /  syn0_tauRise ? Note units of all quantities used here need to be consistent!
    rate_syn0_B = - syn0_B  /  syn0_tauDecay ? Note units of all quantities used here need to be consistent!
    
     
    
}


: Returns a float between 0 and max; implementation of random() as used in LEMS
FUNCTION random_float(max) {
    
    : This is not ideal, getting an exponential dist random number and then turning back to uniform
    : However this is the easiest what to ensure mod files with random methods fit into NEURON's
    : internal framework for managing internal number generation.
    random_float = exp(-1*erand())*max
    
}

:****************************************************
: Methods copied from netstim.mod in NEURON source

 
PROCEDURE seed(x) {
	set_seed(x)
}

VERBATIM
double nrn_random_pick(void* r);
void* nrn_random_arg(int argpos);
ENDVERBATIM


FUNCTION erand() {
VERBATIM
	if (_p_donotuse) {
		/*
		:Supports separate independent but reproducible streams for
		: each instance. However, the corresponding hoc Random
		: distribution MUST be set to Random.negexp(1)
		*/
		_lerand = nrn_random_pick(_p_donotuse);
	}else{
		/* only can be used in main thread */
		if (_nt != nrn_threads) {
           hoc_execerror("multithread random in NetStim"," only via hoc Random");
		}
ENDVERBATIM
		: the old standby. Cannot use if reproducible parallel sim
		: independent of nhost or which host this instance is on
		: is desired, since each instance on this cpu draws from
		: the same stream
		erand = exprand(1)
VERBATIM
	}
ENDVERBATIM
}

PROCEDURE noiseFromRandom() {
VERBATIM
 {
	void** pv = (void**)(&_p_donotuse);
	if (ifarg(1)) {
		*pv = nrn_random_arg(1);
	}else{
		*pv = (void*)0;
	}
 }
ENDVERBATIM
}

: End of methods copied from netstim.mod in NEURON source
:****************************************************

