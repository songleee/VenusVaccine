import torch
import os
import json
import numpy as np
import argparse
from tqdm import tqdm

def e_descriptor_embedding(seq):
    e1 = {'A': 0.008, 'R': 0.171, 'N': 0.255, 'D': 0.303, 'C': -0.132, 'Q': 0.149, 'E': 0.221, 'G': 0.218,
        'H': 0.023, 'I': -0.353, 'L': -0.267, 'K': 0.243, 'M': -0.239, 'F': -0.329, 'P': 0.173, 'S': 0.199,
        'T': 0.068, 'W': -0.296, 'Y': -0.141, 'V': -0.274}
    e2 = {'A': 0.134, 'R': -0.361, 'N': 0.038, 'D': -0.057, 'C': 0.174, 'Q': -0.184, 'E': -0.28, 'G': 0.562,
        'H': -0.177, 'I': 0.071, 'L': 0.018, 'K': -0.339, 'M': -0.141, 'F': -0.023, 'P': 0.286, 'S': 0.238,
        'T': 0.147, 'W': -0.186, 'Y': -0.057, 'V': 0.136}
    e3 = {'A': -0.475, 'R': 0.107, 'N': 0.117, 'D': -0.014, 'C': 0.07, 'Q': -0.03, 'E': -0.315, 'G': -0.024,
        'H': 0.041, 'I': -0.088, 'L': -0.265, 'K': -0.044, 'M': -0.155, 'F': 0.072, 'P': 0.407, 'S': -0.015,
        'T': -0.015, 'W': 0.389, 'Y': 0.425, 'V': -0.187}
    e4 = {'A': -0.039, 'R': -0.258, 'N': 0.118, 'D': 0.225, 'C': 0.565, 'Q': 0.035, 'E': 0.157, 'G': 0.018,
        'H': 0.28, 'I': -0.195, 'L': -0.274, 'K': -0.325, 'M': 0.321, 'F': -0.002, 'P': -0.215, 'S': -0.068,
        'T': -0.132, 'W': 0.083, 'Y': -0.096, 'V': -0.196}
    e5 = {'A': 0.181, 'R': -0.364, 'N': -0.055, 'D': 0.156, 'C': -0.374, 'Q': -0.112, 'E': 0.303, 'G': 0.106,
        'H': -0.021, 'I': -0.107, 'L': 0.206, 'K': -0.027, 'M': 0.077, 'F': 0.208, 'P': 0.384, 'S': -0.196,
        'T': -0.274, 'W': 0.297, 'Y': -0.091, 'V': -0.299}
    # Build descriptor tensors
    descriptor_dicts = [e1, e2, e3, e4, e5]
    descriptors = {}
    for aa in e1.keys():
        descriptors[aa] = [d[aa] for d in descriptor_dicts]
    seq_embeds = [descriptors.get(aa, [0.0]*5) for aa in seq]
    return seq_embeds

def z_descriptor_embedding(seq):
    z1 = {'A': 0.07, 'R': 2.88, 'N': 3.22, 'D': 3.64, 'C': 0.71, 'Q': 2.18, 'E': 3.08, 'G': 2.23, 'H': 2.41,
        'I': -4.44, 'L': -4.19, 'K': 2.84, 'M': -2.49, 'F': -4.92, 'P': -1.22, 'S': 1.96, 'T': 0.92, 'W': -4.75,
        'Y': -1.39, 'V': -2.69}
    z2 = {'A': -1.73, 'R': 2.52, 'N': 1.45, 'D': 1.13, 'C': -0.97, 'Q': 0.53, 'E': 0.39, 'G': -5.36, 'H': 1.74,
        'I': -1.68, 'L': -1.03, 'K': 1.41, 'M': -0.27, 'F': 1.30, 'P': 0.88, 'S': -1.63, 'T': -2.09, 'W': 3.65,
        'Y': 2.32, 'V': -2.53}
    z3 = {'A': 0.09, 'R': -3.44, 'N': 0.84, 'D': 2.36, 'C': 4.13, 'Q': -1.14, 'E': -0.07, 'G': 0.30, 'H': 1.11,
        'I': -1.03, 'L': -0.98, 'K': -3.14, 'M': -0.41, 'F': 0.45, 'P': 2.23, 'S': 0.57, 'T': -1.40, 'W': 0.85,
        'Y': 0.01, 'V': -1.29}
    # Build descriptor tensors
    descriptor_dicts = [z1, z2, z3]
    descriptors = {}
    for aa in z1.keys():
        descriptors[aa] = [d[aa] for d in descriptor_dicts]
    seq_embeds = [descriptors.get(aa, [0.0]*3) for aa in seq]
    return seq_embeds

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file', type=str, default='data')
    args = parser.parse_args()
    # Load data  
    new_list = []
    for l in tqdm(open(args.json_file)):
        l = json.loads(l)
        seq = l['aa_seq']
        e_descriptor = e_descriptor_embedding(seq)
        z_descriptor = z_descriptor_embedding(seq)
        new_list.append({**l, 'e_descriptor': e_descriptor, 'z_descriptor': z_descriptor})
    # Save data
    with open(args.json_file, 'w') as f:
        for l in new_list:
            f.write(json.dumps(l) + '\n')