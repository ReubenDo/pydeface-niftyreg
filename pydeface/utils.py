"""Utility scripts for pydeface."""

import os
import shutil
import sys
from pkg_resources import resource_filename, Requirement
import tempfile
import numpy as np
from nipype.interfaces import niftyreg
from nibabel import load, Nifti1Image
from shutil import copyfile


def initial_checks(template=None, facemask=None):
    """Initial sanity checks."""
    if template is None:
        template = resource_filename(Requirement.parse("pydeface"),
                                     "pydeface/data/mean_reg2mean.nii.gz")
    if facemask is None:
        facemask = resource_filename(Requirement.parse("pydeface"),
                                     "pydeface/data/facemask.nii.gz")

    if not os.path.exists(template):
        raise Exception('Missing template: %s' % template)
    if not os.path.exists(facemask):
        raise Exception('Missing face mask: %s' % facemask)

        sys.exit(2)
    return template, facemask


def output_checks(infile, outfile=None, outfolder=None, force=False):
    """Determine output file name."""
    if force is None:
        force = False
        
    if outfile is None:
        if not outfolder is None:
            outfile = os.path.join(outfolder,  os.path.basename(infile))
        else:
            outfile = infile.replace('.nii', '_defaced.nii')
            
        print(outfile)

    if os.path.exists(outfile) and force:
        print('Previous output will be overwritten.')
    elif os.path.exists(outfile):
        raise Exception("%s already exists. Remove it first or use '--force' "
                        "flag to overwrite." % outfile)
    else:
        pass
    return outfile


def generate_tmpfiles(verbose=True):
    _, tmp_infile = tempfile.mkstemp(suffix='.nii.gz')
    _, template_reg_mat = tempfile.mkstemp(suffix='.mat')
    _, warped_mask = tempfile.mkstemp(suffix='.nii.gz')
    if verbose:
        print("Temporary files:\n  %s\n  %s\n  %s" % (tmp_infile, template_reg_mat, warped_mask))
    _, template_reg = tempfile.mkstemp(suffix='.nii.gz')
    _, warped_mask_mat = tempfile.mkstemp(suffix='.mat')
    return tmp_infile, template_reg, template_reg_mat, warped_mask, warped_mask_mat


def cleanup_files(*args):
    print("Cleaning up...")
    for p in args:
        if os.path.exists(p):
            os.remove(p)


def get_outfile_type(outpath):
    # Returns fsl output type for passing to fsl's flirt
    if outpath.endswith('nii.gz'):
        return 'NIFTI_GZ'
    elif outpath.endswith('nii'):
        return 'NIFTI'
    else:
        raise ValueError('outfile path should be have .nii or .nii.gz suffix')


def deface_image(infile=None, outfile=None, outfolder=None, facemask=None,
                 template=None, force=False,
                 forcecleanup=False, verbose=True, **kwargs):
    if not infile:
        raise ValueError("infile must be specified")
    if shutil.which('reg_aladin') is None:
        raise EnvironmentError("reg_aladin cannot be found on the path")
    else:
        print("Niftyreg has been found")

    template, facemask = initial_checks(template, facemask)
    outfile = output_checks(infile, outfile, outfolder, force)
    tmp_infile, template_reg, template_reg_mat, warped_mask, warped_mask_mat = generate_tmpfiles()
    
    copyfile(infile, tmp_infile)

    print('Defacing...\n  %s' % infile)
    # register template to infile
    node = niftyreg.RegAladin()
    node.inputs.ref_file = tmp_infile
    node.inputs.flo_file = template
    node.inputs.aff_file = template_reg_mat
    node.inputs.res_file = warped_mask
    if not verbose:
        node.inputs.verbosity_off_flag = True
    node.run()


    # warp facemask to infile
    node = niftyreg.RegResample()
    node.inputs.ref_file = tmp_infile
    node.inputs.flo_file = facemask
    node.inputs.trans_file = template_reg_mat
    node.inputs.out_file = warped_mask
    node.inputs.inter_val = 'NN'
    if not verbose:
        node.inputs.verbosity_off_flag = True
    node.run()


    # multiply mask by infile and save
    infile_img = load(tmp_infile)
    warped_mask_img = load(warped_mask)
    try:
        outdata = infile_img.get_fdata().squeeze() * warped_mask_img.get_fdata()
    except ValueError:
        tmpdata = np.stack([warped_mask_img.get_fdata()] *
                           infile_img.get_fdata().shape[-1], axis=-1)
        outdata = infile_img.get_fdata() * tmpdata

    masked_brain = Nifti1Image(outdata, infile_img.affine,
                               infile_img.header)
    masked_brain.to_filename(outfile)
    print("Defaced image saved as:\n  %s" % outfile)

    if forcecleanup:
        cleanup_files(tmp_infile, warped_mask, template_reg, template_reg_mat)
        return warped_mask_img
    else:
        return tmp_infile, warped_mask, template_reg, template_reg_mat
