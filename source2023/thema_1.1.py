from huffman import *
from imageFunction import *
from videoFunction import *

videoPath = '../auxiliary2023/OriginalVideos/thema_1.avi'


def videoEncoder():
    """
        Encode the video
    """
    # ------------------------------- Load Video Properties -------------------------------- #
    # Read the video
    frames, videoProperties = openVideo(videoPath)
    print(
        f'The video has {len(frames)} frames, a height of {videoProperties[2]} pixels, a width of'
        f' {videoProperties[1]} pixels and a framerate of {videoProperties[3]} frames per second.')

    # Convert the video to grayscale
    frames = createGrayscaleVideo(frames)

    width = videoProperties[1]
    height = videoProperties[2]
    fps = videoProperties[3]

    # The grayscale original video
    createVideoOutput(frames, width, height, fps, 'thema_1_1_originalGrayScaleVideo.avi')
    print('Original grayscale video exported successfully!')

    # Add all the frames to the original frames list
    originalFrames = [frames]
    H = entropyScore(originalFrames)
    print('Entropy of the original grayscale video is: ', H)

    # Create the video of the error frames sequence
    seqErrorImages = calSeqErrorImages(frames)
    createVideoOutput(seqErrorImages, width, height, fps, 'thema_1_1_seqErrorFrames.avi')

    # Huffman encoding
    # Create the Huffman tree
    huffmanTree = createHuffmanTree(seqErrorImages)
    print('\tHuffman tree created successfully!')

    # Create the Huffman table
    huffmanTable = createHuffmanTable(huffmanTree)
    print('\tHuffman table created successfully!')

    # Encode the error frames sequence
    encodedSeqErrorImages = encodeHuffman(seqErrorImages, huffmanTable)

    # Save the encoded error frames sequence
    videoSpecs = np.array([len(frames), width, height, fps], dtype='float64')

    saveEncodedData(encodedSeqErrorImages, 'thema_1_1_encodedSF.pkl')
    saveEncodedData(huffmanTable, 'thema_1_1_hT.pkl')
    saveEncodedData(videoSpecs, 'thema_1_1_vS.pkl')

    print('\tEncoded video properties exported successfully!')

    # Return the entropy of the original grayscale video
    return H


def videoDecoder():
    """
        Decode the video
    """
    encodedSeqErrorImages = readEncodedData('thema_1_1_encodedSF.pkl')
    huffmanTable = readEncodedData('thema_1_1_hT.pkl')
    videoSpecs = readEncodedData('thema_1_1_vS.pkl')

    print('\tEncoded video properties imported successfully!')
    width = int(videoSpecs[1])
    height = int(videoSpecs[2])
    fps = float(videoSpecs[3])

    # Huffman decoding
    # Decode the error frames sequence
    frames = decodeHuffman(encodedSeqErrorImages, huffmanTable, width, height)

    print(
        f'The video has {len(frames)} frames, a height of {height} pixels, a width of {width} pixels and a framerate of'
        f' {fps} frames per second.')

    firstFrameFlag = True

    decodedFrames = []

    # Recreate the frames of the original video
    prevFrame = None
    i = 0
    for frame in frames:
        if firstFrameFlag:
            decodedFrames.append(frame)
            saveImage(frame, str(i) + '.jpg')
            prevFrame = frame
            firstFrameFlag = False
        else:
            decodedFrame = prevFrame + frame  # Add frame to prevFrame
            saveImage(decodedFrame, str(i) + '.jpg')
            decodedFrames.append(decodedFrame)
            prevFrame = decodedFrame
        i += 1

    # Convert the list to a numpy array
    decodedFrames = np.array(decodedFrames, dtype='uint8')

    # Create the video of the decoded frames
    createVideoOutput(decodedFrames, width, height, fps, 'thema_1_1_decodedVideo.avi')
    print('Decoded grayscale video exported successfully!')

    H = entropyScore(decodedFrames)
    print('Entropy of the decoded grayscale video is: ', H)

    # Return the entropy of the original grayscale video
    return H


if __name__ == '__main__':
    entropy1 = videoEncoder()
    entropy2 = videoDecoder()
    if entropy1 == entropy2:
        print('The decoded video is the same as the original video!')
    else:
        print('The decoded video is not the same as the original video! Something went wrong!')
