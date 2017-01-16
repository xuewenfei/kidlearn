from .hssbg import *  # HierarchicalSSBG
from .riarit import *  # RiaritHssbg
from .zpdes import *  # ZpdesHssbg
from .teacher_sequence import Sequence
from .random_sequence import RandomSequence
from .pomdp import POMDP, perseus
from .linucb_d import LinUCB
from .linucb_h import HybridUCB

seq_dict_gen = {}
seq_dict_gen["RiaritHssbg"] = RiaritHssbg
seq_dict_gen["RiaritSsbg"] = RiaritSsbg
seq_dict_gen["ZpdesHssbg"] = ZpdesHssbg
seq_dict_gen["ZpdesSsbg"] = ZpdesSsbg
seq_dict_gen["Sequence"] = Sequence
seq_dict_gen["RandomSequence"] = RandomSequence
seq_dict_gen["POMDP"] = POMDP
