import pandas as pd
import numpy as np
import category_encoders as ce
from sklearn.model_selection import train_test_split
from keras import models, layers, initializers
from keras.utils.np_utils import to_categorical

res_pd = pd.read_csv('./data.csv', encoding='utf-8')#学習データ読み込み
#以下のリストをワンホットエンコーディング
ohe_cols = ['性別', '種別', '回り方', '距離', '天気', '状態']
ce_ohe = ce.OneHotEncoder(cols=ohe_cols, handle_unknown='Nan')
a = ce_ohe.fit(res_pd)
res_pd = a.transform(res_pd)
#以下のリストはラベル化(カテゴリ値で処理)
ce_list = ['馬名', '父親', '母親', '騎手', '調教師']
ce_oe = ce.OrdinalEncoder(cols=ce_list, handle_unknown='Nan')
b = ce_oe.fit(res_pd)
res_pd = b.transform(res_pd)
#0が存在しないので-1して0を作り出す
res_pd['馬名'] = res_pd['馬名'] - 1
res_pd['父親'] = res_pd['父親'] - 1
res_pd['母親'] = res_pd['母親'] - 1
res_pd['騎手'] = res_pd['騎手'] - 1
res_pd['調教師'] = res_pd['調教師'] - 1
X = res_pd.drop('着順', axis=1).to_numpy()
y = (res_pd['着順']-1).to_numpy()

y_ohe = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_ohe, test_size=0.2, random_state=42)

model = models.Sequential()
model.add(layers.Dense(512, kernel_initializer='he_normal', input_shape=(38,)))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))

model.add(layers.Dense(256, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))
model.add(layers.Dropout(0.3))

model.add(layers.Dense(128, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))

model.add(layers.Dense(128, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))

model.add(layers.Dense(64, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))
model.add(layers.Dropout(0.2))

model.add(layers.Dense(128, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))

model.add(layers.Dense(32, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))
model.add(layers.Dropout(0.2))
                            
model.add(layers.Dense(32, kernel_initializer='he_normal'))
model.add(layers.BatchNormalization())
model.add(layers.core.Activation('relu'))
                                        
model.add(layers.Dense(64, kernel_initializer='he_normal'))
model.add(layers.core.Activation('relu'))
model.add(layers.Dropout(0.2))

model.add(layers.Dense(18, activation='softmax'))
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X, y_ohe, epochs=40, batch_size=20)

predict_data = pd.read_csv('./race_data.csv', encoding='utf-8')#予想データ読み込み
predict_data = a.transform(predict_data)
predict_data = b.transform(predict_data)

column = predict_data.columns.tolist()
for i, con in enumerate(['馬名', '父親', '母親', '騎手', '調教師']):
    if predict_data[con].isnull().sum() != 0:
        num = b.mapping[i]['mapping'][-2]+1
        for j in range(len(predict_data)):
            if np.isnan(predict_data.iloc[j, column.index(con)]):
                predict_data.iloc[j, 2] = num
                num += 1


predict_data['馬名'] = predict_data['馬名'] - 1
predict_data['父親'] = predict_data['父親'] - 1
predict_data['母親'] = predict_data['母親'] - 1
predict_data['騎手'] = predict_data['騎手'] - 1
predict_data['調教師'] = predict_data['調教師'] - 1
predict_data = predict_data.drop('着順', axis=1)

result = model.predict(predict_data)

for i, res in enumerate(result):
    print('馬番:'+str(i+1)+'の馬が'+str(np.argmax(res)+1)+'位と予測')