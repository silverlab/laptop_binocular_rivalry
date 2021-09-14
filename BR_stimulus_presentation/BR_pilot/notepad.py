#    topImage, bottomImage = makeGratingStimuliForRivalry(topOrientation,botOrientation, topColor, botColor, 256*2)
#        
#    
#    bottomStim = visual.ImageStim(win, mask="circle", image=bottomImage, size=(gratingSize, gratingSize), opacity=1.0)# color='red')
#    bottomStim.draw()
#    topStim = visual.ImageStim(win, mask="circle", image=topImage, size=(gratingSize, gratingSize), opacity=0.5)# color='red')
#    topStim.draw()
#    
#    win.flip()
#    # run key data
#    waitForKeys = True
#    kb.clock.reset()
#    while waitForKeys:
#        responseKeys = ['right', 'left', 'quit']
#        keys = kb.getKeys( waitRelease=True)
#        if 'q' in keys:
#            win.close()
#            core.quit()
#            break
#        for key in keys:
#            if key in responseKeys:
#                thisReactionTime = key.rt
#                thisChoice = key.name
#                print(key.name, key.rt, key.duration, key.tDown)
#                waitForKeys = False
#                break
#            else:
#                # beep for incorrect key
#                wrongKeyNote.play()
#                
#    
#    trials.data.add('RT', thisReactionTime)  # add the data to our set
#    trials.data.add('choice', thisChoice)
#    nDone += 1  # just for a quick reference
