import pickle,re,os
import xml.dom.minidom as md
UI='/tmp/fm6/fm6ui'; W=2580; S=330; K='1.34375'
new=pickle.load(open('/tmp/fm6/other.pkl','rb'))   # current device state (my v0.5 + parallel car/bg fixes)
def get(f): return new.get(f) or open(os.path.join(UI,f),'rb').read().decode('latin-1')
log=[]
def rep(f,a,b,cnt=1):
    t=get(f); n=t.count(a); assert n==cnt,(f,a[:90],n); new[f]=t.replace(a,b); log.append((f,a[:50]))
P='Scenes/WPF/'
# 2) Meine Autos: owned-car big thumbnail is rendered squeezed -> ScaleX in garage/livery states
f=P+'F111_ModelSelect.xaml'
rep(f,'''<Image x:Name="Image_ThumbnailLarge" Tag="{Binding Installed}"''','''<Image x:Name="Image_ThumbnailLarge" RenderTransformOrigin="0.5,1" Tag="{Binding Installed}"''')
rep(f,'''Source="{Binding BigThumbnail}" MaxWidth="816" HorizontalAlignment="Center" Margin="40,0,0,100"/>''','''Source="{Binding BigThumbnail}" MaxWidth="816" HorizontalAlignment="Center" Margin="40,0,0,100"><Image.RenderTransform><ScaleTransform/></Image.RenderTransform></Image>''')
anim='''
                        <DoubleAnimationUsingKeyFrames Storyboard.TargetProperty="(UIElement.RenderTransform).(ScaleTransform.ScaleX)" Storyboard.TargetName="Image_ThumbnailLarge">
                            <DiscreteDoubleKeyFrame KeyTime="0" Value="%s"/>
                        </DoubleAnimationUsingKeyFrames>'''%K
t=get(f)
for st in ('CareerGarageVisualState','FreeplayGarageVisualState','LiveryCarSelectState'):
    i=t.index('<VisualState x:Name="%s">'%st); j=t.index('<Storyboard>',i); assert j-i<120,st
    j+=len('<Storyboard>'); t=t[:j]+anim.replace('\n','\r\n')+t[j:]
new[f]=t
# 3) other player-car renders
rep(P+'F311_MultiplayerLobby.xaml','<Image x:Name="CarImage" Source="{Binding CarImage}" Stretch="Uniform"/>','<Image x:Name="CarImage" Source="{Binding CarImage}" Stretch="Uniform" RenderTransformOrigin="0.5,0.5"><Image.RenderTransform><ScaleTransform ScaleX="%s"/></Image.RenderTransform></Image>'%K)
rep(P+'F800_Profile.xaml','<Image x:Name="Image_PlayerCar" Source="{Binding CarImage}" Width="816" Height="459" HorizontalAlignment="Left" Margin="130,0,0,0"/>','<Image x:Name="Image_PlayerCar" Source="{Binding CarImage}" Width="816" Height="459" HorizontalAlignment="Left" Margin="130,0,0,0" RenderTransformOrigin="0.5,0.5"><Image.RenderTransform><ScaleTransform ScaleX="%s"/></Image.RenderTransform></Image>'%K)
# 4) pages declared 1920 wide -> full width (their LayoutRoot is already full width)
import glob
for p in glob.glob(UI+'/Scenes/WPF/*.xaml'):
    f=P+os.path.basename(p); t=get(f)
    k=t.find('<Page.Resources>'); k=k if k>0 else t.find('>',t.find('<Page'))+1
    head=t[:k]
    if re.match(r'F7(0|1)\d_',os.path.basename(p)): continue
    if '<Page' in head and 'Width="{StaticResource MaxSceneWidth}"' in head:
        new[f]=head.replace('Width="{StaticResource MaxSceneWidth}"','Width="{StaticResource FullSceneWidth}"',1)+t[k:]; log.append((f,'Page width'))
# 5) telemetry menu is HUD -> 21:9 corner (+90 instead of +330)
f=P+'F936_Telemetry.xaml'; t=get(f)
if 'x:Name="Menu" Canvas.Left="447"' in t: rep(f,'x:Name="Menu" Canvas.Left="447"','x:Name="Menu" Canvas.Left="207"')
bad=[f for f,t in new.items() if not (lambda s: (md.parseString(s.encode('latin-1')) and True))(t)]
# Autovista panels (rendered into 3D panels) stay original
for f in [k for k in new if re.match(r'Scenes/WPF/F7(0|1)\d_',k)]: del new[f]; log.append((f,'reverted to original'))
# F041: logo/message as designed (+330 centred), page now full width
f=P+'F041_Loading.xaml'; t=get(f); t=re.sub(r'(x:Name="Image_LogoForza" Canvas.Left=")\d+',r'\g<1>1344',t); t=re.sub(r'(x:Name="MessageContainer" Canvas.Left=")\d+',r'\g<1>1192',t); new[f]=t
pickle.dump(new,open('/tmp/fm6/new_v6.pkl','wb'))
print(len(new),'files'); [print(x) for x in log]
