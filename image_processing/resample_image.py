import os
import SimpleITK as sitk
import numpy as np
import nibabel as nib

def read_image(path):
    reader = sitk.ImageFileReader()
    reader.SetFileName(path)
    image = reader.Execute()
    return image

def normalize(image):
    """
    Normalize an image to 0 - 255 (8bits)
    """
    normalizeFilter = sitk.NormalizeImageFilter()
    resacleFilter = sitk.RescaleIntensityImageFilter()
    resacleFilter.SetOutputMaximum(255)
    resacleFilter.SetOutputMinimum(0)

    image = normalizeFilter.Execute(image)  # set mean and std deviation
    image = resacleFilter.Execute(image)  # set intensity 0-255

    return image

def resize(image, new_size):
    return sitk.Resample(image, new_size, interpolator=sitk.sitkLinear)

def downsample(image, resize_factor, interpolator):

    dimension = image.GetDimension()
    reference_physical_size = np.zeros(image.GetDimension())
    reference_physical_size[:] = [(sz-1)*spc if sz*spc>mx  else mx for sz,spc,mx in zip(image.GetSize(), image.GetSpacing(), reference_physical_size)]
    
    reference_origin = image.GetOrigin()
    reference_direction = image.GetDirection()

    reference_size = [round(sz/resize_factor) for sz in image.GetSize()] 
    reference_spacing = [ phys_sz/(sz-1) for sz,phys_sz in zip(reference_size, reference_physical_size) ]

    reference_image = sitk.Image(reference_size, image.GetPixelIDValue())
    reference_image.SetOrigin(reference_origin)
    reference_image.SetSpacing(reference_spacing)
    reference_image.SetDirection(reference_direction)

    reference_center = np.array(reference_image.TransformContinuousIndexToPhysicalPoint(np.array(reference_image.GetSize())/2.0))
    
    transform = sitk.AffineTransform(dimension)
    transform.SetMatrix(image.GetDirection())

    transform.SetTranslation(np.array(image.GetOrigin()) - reference_origin)
  
    centering_transform = sitk.TranslationTransform(dimension)
    img_center = np.array(image.TransformContinuousIndexToPhysicalPoint(np.array(image.GetSize())/2.0))
    centering_transform.SetOffset(np.array(transform.GetInverse().TransformPoint(img_center) - reference_center))
    # centered_transform = sitk.Transform(transform)
    centered_transform = sitk.CompositeTransform([sitk.Transform(transform), sitk.Transform(centering_transform)])

    # sitk.Show(sitk.Resample(original_CT, reference_image, centered_transform, sitk.sitkLinear, 0.0))
    
    return sitk.Resample(image, reference_image, centered_transform, interpolator, 0.0)


def preprocess(src, dst, mask=False):
    for fname in os.listdir(src):
        image = read_image(os.path.join(src, fname))
        # image = resize(image, [128, 128, 128])
        if mask:
            image = downsample(image, 2.0, sitk.sitkNearestNeighbor)
        else:
            image = downsample(image, 2.0, sitk.sitkLinear)

        if not mask:
            image = normalize(image)

        sitk.WriteImage(image, os.path.join(dst, fname))


def check_image(img):
    image = read_image(img)
    image_mtx = sitk.GetArrayFromImage(image)
    print(image_mtx.shape)


if __name__ == '__main__':
    src = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks_b'
    dst = '/data/hohokam/Yanxi/Data/mri2pet/adni/masks_d'
    # preprocess(src, dst, mask=True)
    check_image(os.path.join(dst, 'm941S4764L060112E73T.nii'))