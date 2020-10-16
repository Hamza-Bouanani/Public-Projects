def hier(nb_fl,nb_c1,nb_c2,nb_c3,batch,val_split):
    inputs=Input(shape=(512,))
    
    first_layer=Dense(nb_fl,activation='sigmoid')(inputs)
    
    g3=Dense(1,activation='sigmoid')(first_layer)
    
    c1=Dense(nb_c1,activation='sigmoid')(first_layer)
    
    g1=Dense(1,activation='sigmoid')(c1)
    
    c2=Dense(nb_c2,activation='sigmoid')(c1)
    
    g2=Dense(1,activation='sigmoid')(c2)
    
    c3=Dense(nb_c3,activation='sigmoid')(c2)
    
    g0=Dense(1,activation='sigmoid')(c3)
    
    g4=Dense(1,activation='sigmoid')(c3)
    
    
    loss_f='binary_crossentropy'
    
    model = Model(inputs=[inputs], outputs=[g0,g1,g2,g3,g4])
    model.compile(optimizer='Adam', loss= [loss_f,loss_f,loss_f,loss_f,loss_f])

    return model


