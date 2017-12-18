import keras
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np
import tensorflow as tf

model = keras.applications.inception_v3.InceptionV3(include_top=True,
                                                    weights='imagenet',
                                                    input_tensor=None,
                                                    input_shape=None)
graph = tf.get_default_graph()


def predict(image_file):
    img = image.load_img(image_file, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    x = preprocess_input(x)

    global graph
    with graph.as_default():
        preds = model.predict(x)
    top3 = decode_predictions(preds, top=3)[0]
    answer = dict(zip(('label', 'description', 'probability'), top3[0]))
    print(answer)
    predictions = [{'label': label, 'description': description, 'probability': round(probability, 2)}
                    for label, description, probability in top3]
    return {'answer': {'label': answer['label'],
                       'description': answer['description'],
                       'probability': round(answer['probability'], 2)},
            'top3': predictions}