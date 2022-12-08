
## Structure du programme 


### Installation:

**Dans pycharm :** \
CTRL+ALT+s, puis choisir project -> python interpreter et + puis likeprocessing

**dans le terminal :** \
pip install likeprocessing


### Les fonctions setup(), draw() et run(globals())

Le programme doit contenir deux fonctions, setup() et draw(), et l'exécution est lancée à l'aide de l'instruction run(globals()).

Lorsque l'on exécute l'instruction run(globals()), la fonction setup() est exécutée une fois :


```
from likeprocessing.processing import *
def setup():
    createCanvas(800,600)
    # instructions de paramétrage de l'affichage
```


Cette fonction permet de définir les dimensions de la fenêtre de tracé, et quelques paramètres initiaux. Les valeurs données aux paramètres de la fonction **createCanvas() ** sont affectées automatiquement à deux variables systèmes : **width** pour le premier paramètre et **height** pour le second. Un troisième paramètre **resizable** optionnel permet d'offrir la possibilité de redimensionner la fenêtre avec la souris  On peut récupérer les valeurs de **width** et **height** grâce au fonction **width()** et **height()**

Puis la fonction **draw()** est ensuite exécutée en boucle, après l'exécution de **setup()**:


```
def draw():
    # instructions de dessin
```


Elle contient des instructions qui seront exécutées avec une fréquence réglable, permettant de modifier le contenu de la fenêtre et de créer des contenus statiques ou des animations.

L'instruction **stop()** met fin à l'exécution de la boucle :


```
def compute():
    # instructions de calcul
```


Cette fonction n'est pas obligatoire. Elle permet d'éviter de trop surcharger la fonction **draw()** en réservant celle-ci aux instructions de dessins. La fonction **compute()** si elle existe est insérée dans la boucle et est exécutée avant la fonction **draw()** 


## Structure de base :


```
from likeprocessing.processing import *

def setup():
   createCanvas(400,200)
   background("grey")

def draw():
   pass

run(globals())
```



## Fonctions système


<table>
  <tr>
   <td><strong>Fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>width(), height()
   </td>
   <td>Dimensions de la zone de dessin. Les valeurs de width et height sont définies par les paramètres de la fonction createCanvas().
   </td>
  </tr>
</table>



## Rafraîchissement


<table>
  <tr>
   <td><strong>Fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>frameCount()
   </td>
   <td>Nombre d'images affichées depuis le démarrage du programme.
   </td>
  </tr>
  <tr>
   <td>frameRate() \
getFrameRate()
   </td>
   <td>Renvoie le nombre d'images affichées chaque seconde.
   </td>
  </tr>
  <tr>
   <td>frameRate(valeur) \
setFrameRate(valeur)
   </td>
   <td>Spécifie le nombre d'images à afficher chaque seconde.
   </td>
  </tr>
  <tr>
   <td>noLoop()
   </td>
   <td>Si cette instruction est présente dans la fonction setup la fonction draw sera exécutée une seule fois. Si cette instruction est présente dans la fonction draw, les instructions de la fonction draw en cours sont exécutées (il n'y a pas d'interruption) mais celle-ci ne sera pas appelée à nouveau.
   </td>
  </tr>
  <tr>
   <td>loop()
   </td>
   <td>Relance l'exécution en boucle de draw().
   </td>
  </tr>
</table>



## Couleurs


## Désigner une couleur


<table>
  <tr>
   <td><strong>syntaxe</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>'red'
   </td>
   <td>nom de couleur
   </td>
  </tr>
  <tr>
   <td>120
   </td>
   <td>niveau de gris : 0 - 255
   </td>
  </tr>
  <tr>
   <td>(100, 125, 255)
   </td>
   <td>couleur r, v, b (décimal) : 0 - 255
   </td>
  </tr>
  <tr>
   <td>'#2aff95'
   </td>
   <td>couleur r, v, b (hexadécimal) : 00 - ff
   </td>
  </tr>
</table>



## Dessiner en couleur


<table>
  <tr>
   <td><strong>Fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>background(couleur)
   </td>
   <td>Définit la couleur d'arrière-plan de la zone de dessin (255 par défaut).
   </td>
  </tr>
  <tr>
   <td>fill(couleur=None)
   </td>
   <td>Définit la couleur de remplissage des formes (255 par défaut) et réactive le remplissage des formes. Sans paramètre seul le remplissage est activé (utile après un noFill()). Retourne la valeur précédente du remplissage.
   </td>
  </tr>
  <tr>
   <td>get_fill()
   </td>
   <td>Retourne la couleur de fond actuelle
   </td>
  </tr>
  <tr>
   <td>noFill()
   </td>
   <td>Désactive la couleur de remplissage.
   </td>
  </tr>
  <tr>
   <td>stroke(couleur)
   </td>
   <td>Définit la couleur du tracé des bords des formes et des lignes("black" par défaut). Retourne la valeur précédente de la couleur.
   </td>
  </tr>
  <tr>
   <td>get_stroke()
   </td>
   <td>retourne la couleur des bords actuelle
   </td>
  </tr>
  <tr>
   <td>noStroke()
   </td>
   <td>Désactive le tracé du contour des figures. Retourne la valeur précédente de la couleur.
   </td>
  </tr>
  <tr>
   <td>save_fill_stroke()
   </td>
   <td>Sauvegarde les paramètres fill et stroke
   </td>
  </tr>
  <tr>
   <td>restore_fill_stroke()
   </td>
   <td>recharge les paramètres fill et stroke précédemment sauvegardé avec <strong>save_fill_stroke</strong>
   </td>
  </tr>
</table>


Si **noFill()** et **noStroke() **sont exécutées en même temps, rien n'est tracé dans la zone de dessin.


## Formes


### Primitives 2d

L'origine du repère est située en haut à gauche. Les abscisses augmentent de gauche à droite, les ordonnées augmentent de haut en bas.



![](./images/image1.png)



<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>point(x, y)
   </td>
   <td>Trace un point de coordonnées (x, y). carré de 2x2 pixels
   </td>
  </tr>
  <tr>
   <td>line(x1, y1, x2, y2)
   </td>
   <td>Trace un segment reliant les deux points de coordonnées (x1, y1) et (x2, y2).
   </td>
  </tr>
  <tr>
   <td>ellipse(x, y, largeur, hauteur)
   </td>
   <td>Tracer une ellipse dont le centre a pour coordonnées (x, y) et dont la largeur et la hauteur prennent les valeurs fixées.
   </td>
  </tr>
  <tr>
   <td>circle(x, y, diametre)
   </td>
   <td>Trace un cercle dont le centre a pour coordonnées (x, y) et dont le diamètre prend la valeur fixée. Idem ellipse((x, y, diametre, diametre)
   </td>
  </tr>
  <tr>
   <td>arc(x,y,largeur,hauteur,,angleDebut, angleFin)
   </td>
   <td>Créer une portion d'ellipse type part de tarte qui pourra être rempli entre les points repérés par les angles angleDébut et angleFin (unité courante). x et y sont les coordonnées du centre du cercle.  
   </td>
  </tr>
  <tr>
   <td>circle_arc(x,y,rayon,angleDebut, angleFin)
   </td>
   <td>idem arc mais à partir d'un disque
   </td>
  </tr>
  <tr>
   <td>ellipseMode(corners_center: str)
   </td>
   <td>Définie la position des points x et y des fonctions basées sur ellipse. par défaut : "corners" x et y sont les coordonnées du point en haut à gauche du rectangle dans lequel est inscrit l'ellipse. si les paramètre est "center" x et y représente le centre du rectangle. Retourne la valeur précédente du mode.
   </td>
  </tr>
  <tr>
   <td>rect(x, y, largeur, hauteur)
   </td>
   <td>Créer un rectangle aux coordonnées x,y de largeur largeur et de hauteur. Sii rectMode('center') x et y sont les coordonnées du centre du rectangle. Si rectMode('corners') x,y sont les coordonnées du coin haut gauche. Le rectangle est rempli par la couleur définie par fill(couleur). Si le paramètre image est renseigné le fond du rectangle sera occupé pas l'image retaillée aux dimensions du rectangle sauf si largeur et/ou hauteur sont nulles (ou non renseignées). largeur et/ou hauteur seront alors celles de l'image. Les paramètres <strong>allign_h </strong>(left, center et right) et  <strong>allign_v</strong> (top,center et bottom) permettent d'aligner l'image dans un cadre plus grand qu'elle.
   </td>
  </tr>
  <tr>
   <td>square(x, y, cote)
   </td>
   <td>Trace un carré dont le sommet en haut à gauche a pour coordonnées (x, y) et dont le côté prend la valeur fixée. fonctionnement idem rectangle
   </td>
  </tr>
  <tr>
   <td>rectMode(corners_center: str)
   </td>
   <td>Définie la position des points x et y des fonctions basées sur rect. par défaut : "corners" x et y sont les coordonnées du point en haut à gauche du rectangle. si les paramètre est "center" x et y représente le centre du rectangle. Retourne la valeur précédente du mode.
   </td>
  </tr>
  <tr>
   <td>triangle(x1, y1, x2, y2, x3, y3)
   </td>
   <td>Trace un triangle dont les trois sommets ont pour coordonnées (x1, y1), (x2, y2), et (x3, y3).
   </td>
  </tr>
  <tr>
   <td>quad(x1, y1, x2, y2, x3, y3, x4, y4)
   </td>
   <td>Trace un quadrilatère dont les quatre sommets ont pour coordonnées (x1, y1), (x2, y2), (x3, y3) et (x4, y4).
   </td>
  </tr>
  <tr>
   <td>k_line(points)
   </td>
   <td>trace un ligne brisée à partir d'une liste de points [[1,2],[5,6],[8,3],.....]. (nb_point = nb_segments + 1)
   </td>
  </tr>
</table>



### Tracés


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>strokeWeight(epaisseur)
   </td>
   <td>Définit l'épaisseur du tracé en pixels (par défaut : 1 pixel). Retourne la valeur précédente de la largeur du trait
   </td>
  </tr>
  <tr>
   <td>noStroke()
   </td>
   <td>Désactive le tracé du contour des figures en mettant la largeur du bord à 0. Retourne la valeur précédente de la largeur.
   </td>
  </tr>
  <tr>
   <td>stroke(couleur)
   </td>
   <td>Définit la couleur du tracé des bords des formes et des lignes ("black" par défaut). Si aucune valeur n'est passée, celle-ci retourne la couleur actuelle. Retourne la valeur précédente de la couleur.
   </td>
  </tr>
</table>



## Paramètres optionnels:

Les paramètres optionnels sont passés directement dans la fonction et ne concernent que celle-ci: 

fill, no_fill, fill_mouse_on, stroke, stroke_weight.

exemple :


```
triangle(20, 10, 50, 15, 40, 70, fill = "green", fill_mouse_on="yellow", stroke_weight=3)
```


l'ajout de **command = ma_fonction** au paramètre **fill_mouse_on="couleur"** permet d'exécuter la fonction **ma_fonction()**. Si l'on veut attribuer **ma_fonction** à plusieurs formes il est possible d'ajouter le paramètre **name = valeur**. Dans ce cas, la fonction **ma_fonction(name)** sera exécutée . Il faudra créer impérativement soit : 

def ma_fonction():

    pass

ou

def ma_fonction(nom):

    pass


## Textes


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>text(chaine, x, y)
   </td>
   <td>Affiche la chaîne à la position (x, y) dans une boite ajustée. couleur, largeur bord et couleur bord de la boite idem formes. Accepte les paramètres optionnels
   </td>
  </tr>
  <tr>
   <td>text(chaine, x, y, largeur, hauteur)
   </td>
   <td>Affiche la chaîne à la position (x, y) dans une boite de dimensions largeur x hauteur. couleur, largeur bord et couleur bord de la boite idem formes. largeur et hauteur sont optionnels
   </td>
  </tr>
  <tr>
   <td>textAlign(alignement_horizontal)
<p>
textAlign(alignement_horizontal, alignement_vertical)
   </td>
   <td>Spécifie l'alignement horizontal parmi LEFT, CENTER, et RIGHT et l'alignement vertical parmi TOP, BOTTOM, CENTER, et BASELINE
   </td>
  </tr>
  <tr>
   <td>textFont(police)
<p>
textFont(police, taille)
   </td>
   <td>Spécifie la police de caractères et éventuellement sa taille. Retourne la police et la taille précédente 
   </td>
  </tr>
  <tr>
   <td>textSize(taille)
   </td>
   <td>Spécifie la taille de la police de caractères. Retourne la taille précédente de la police
   </td>
  </tr>
  <tr>
   <td>textStyle(style)
   </td>
   <td>Spécifie le style parmi NORMAL, ITALIC, BOLD et BOLDITALIC
   </td>
  </tr>
  <tr>
   <td>textWidth(chaine)
   </td>
   <td>Largeur en pixels de l'affichage de chaîne, dans la police et taille actuelles
   </td>
  </tr>
</table>



## Paramètres optionnels spécifique à text:

Les paramètres optionnels sont passés directement dans la fonction et ne concernent que celle-ci: 

la fonction text possèdes elle aussi des paramètres optionnels qui ne concernent que la fonction en cours : \
**font, font_size, font_color** qui permettent  de définir la police, la taille des caractères ainsi que la couleur de ceux-ci. 

**allign_h et allign_v** permettent de positionner le texte dans la boîte de texte comme **textAllign()**.

**padx et pady** permettent de créer une marge autour du texte (valeur en pixels)  \
exemple : 


```
text("salut les amis",20,30,300,allign_h="center",font="arial",font_size=48,fontTools="green",pady=10)
```


Ce code va afficher "salut les amis" dans un cadre de longueur 300 à la position x=20 et y=30. La hauteur du cadre est calculée en fonction de la hauteur du texte (font_size). **pady=10** ajoute 10 pixels au dessus et en dessous du texte. **Si la hauteur du cadre est donnée, si celle-ci est trop petite le texte sortira du cadre.**


## Événements


### Touches du clavier


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>key()
   </td>
   <td>état des touches du clavier (list)
   </td>
  </tr>
  <tr>
   <td>keyCode()
   </td>
   <td>Code de la dernière touche appuyée.
   </td>
  </tr>
  <tr>
   <td>keyIsPressed()
<p>
isKeyPressed()
   </td>
   <td>Vaut True lorsqu'une touche du clavier est appuyée et False sinon.
   </td>
  </tr>
  <tr>
   <td>keyIsDown(code)
<p>
keyIsDown(touche)
   </td>
   <td>Vaut True si la touche concernée est appuyée et False sinon.
   </td>
  </tr>
</table>



### Souris


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>mouseX(), mouseY()
   </td>
   <td>Coordonnées du pointeur de la souris
   </td>
  </tr>
  <tr>
   <td>mouseXY()
   </td>
   <td>Coordonnées du pointeur de la souris sous forme de tuple
   </td>
  </tr>
  <tr>
   <td>mouseIsPressed()
   </td>
   <td>Vaut True si la souris est cliquée, et False sinon.
   </td>
  </tr>
  <tr>
   <td>fill_mouse_on(couleur:str)
   </td>
   <td>Change la couleur des formes quand on passe la souris dessus. Non actif par défaut.
   </td>
  </tr>
  <tr>
   <td>noFill_mouse_on()
   </td>
   <td>annule l'effet de fill_mouse_on()
   </td>
  </tr>
  <tr>
   <td>mouse_click_down()
   </td>
   <td>renvoie True lors du passage de relâché à appuyé du bouton de la souris.
   </td>
  </tr>
  <tr>
   <td>mouse_click_up()
   </td>
   <td>renvoie True lors du passage de appuyé à relâché du bouton de la souris.
   </td>
  </tr>
  <tr>
   <td>mouse_click()
   </td>
   <td>idem mouseIsPressed()
   </td>
  </tr>
  <tr>
   <td>mouse_wheel_state()
   </td>
   <td>retourne 1 si la roulette de la souris est tournée vers l'avant, -1 vers l'arrière et 0 si elle est immobile.
   </td>
  </tr>
</table>



## Mathématiques


### Angles


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>angleMode(mode_angle:str)
   </td>
   <td>Définit l'unité de mesure des angles. \
 'rad' les angles des fonctions trigonométriques seront pris comme des radians (défaut) \
 'deg' les angles des fonctions trigonométriques seront pris comme des degrés \
'grd' les angles des fonctions trigonométriques seront pris comme des grades \
Une exception est levée en cas d'erreur de paramètre
<p>
si mode_angle == "" la valeur de mode est retournée (str)
   </td>
  </tr>
  <tr>
   <td>cos(), sin(), tan(), acos(),asin(),atan(),atan2()
   </td>
   <td>Fonctions trigonométriques usuelles l'unité considérée sera celle choisie avec angleMode(). atan2 : même fonctionnement que la fonction math.atan2 mais l'unité de l'angle retourné dépend  de angleMode()  
   </td>
  </tr>
  <tr>
   <td>degrees(mesure) \
radians(mesure) \
grades(mesure)
   </td>
   <td>Convertit une mesure d'angle en degrés, en radians ou en grades. l'unité de mesure dépend de angleMode(). 
   </td>
  </tr>
  <tr>
   <td>HALF_PI, PI, QUARTER_PI, TWO_PI
   </td>
   <td>Constantes permettant respectivement d'approcher les valeurs de π/2, π, π/4, 2π
   </td>
  </tr>
</table>



### Géométrie


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>dist(x1,y1,x2,y2)
   </td>
   <td>retourne la distance entre deux points
   </td>
  </tr>
  <tr>
   <td>midPoint(x1, y1, x2, y2)
   </td>
   <td>retourne le milieu d'un segment défini par deux points
   </td>
  </tr>
</table>



## Images


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>loadImage(chemin)
   </td>
   <td>Charge une image à partir d'un chemin et crée un objet Image. Si nécessaire, l'image peut être préchargée en plaçant l'appel à la fonction loadImage dans la fonction preload.
   </td>
  </tr>
  <tr>
   <td>background(Image)
   </td>
   <td>Affiche une Image en fond d'écran
   </td>
  </tr>
  <tr>
   <td>image(image, x, y)
   </td>
   <td>Affiche une Image en plaçant le pixel en haut à gauche au point de coordonnées (x, y) dans la zone de dessin.
   </td>
  </tr>
  <tr>
   <td>copy_image(picture: Image, rect=None) -> Image
   </td>
   <td>retourne une copie de picture ou une partie de picture au dimensions de rect
   </td>
  </tr>
  <tr>
   <td>get_pixel_color(picture: Image, pos: tuple) -> tuple
   </td>
   <td>retourne la valeur de la couleur d'un pixel d'une image (picture)
<p>
sous la forme d'un tuple
   </td>
  </tr>
  <tr>
   <td>resize_image(picture:Image,size : tuple
   </td>
   <td>retourne une image redimensionné en fonction de size : (largeur,hauteur) 
   </td>
  </tr>
</table>



## Transformations


<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>translate(x,y)
   </td>
   <td>applique une translation à toutes les fonctions de dessin et d'image. x et y sont des valeurs relatives qui s'ajoutent aux translations précédentes.
<p>
La translation est remise à zéro avant chaque exécution de la fonction draw().
   </td>
  </tr>
  <tr>
   <td>get_translate()
   </td>
   <td>retourne la valeur de la translation sous la forme d'un tuple (x,y)
   </td>
  </tr>
  <tr>
   <td>init_translate()
   </td>
   <td>Force la remise à zéro de la translation. (A utiliser dans la fonction draw() en cas de besoin 
   </td>
  </tr>
  <tr>
   <td>rotate(angle,axis)
   </td>
   <td>applique une rotation &lt;angle> par rapport à &lt;axis>. à toutes les fonctions de dessin et d'image. angle est une valeur absolue. Par défaut axis vaut (0,0). Cette fonction retourne la valeur précédente prise par la fonction sous la forme d'un tuple.
   </td>
  </tr>
  <tr>
   <td>flip_h(axe_h)
   </td>
   <td>entraîne une symétrie horizontale par rapport à la droite y = axe_h
   </td>
  </tr>
  <tr>
   <td>flip_v(axe_v)
   </td>
   <td>entraîne une symétrie verticale par rapport à la droite x = axe_v
   </td>
  </tr>
</table>



## Temporisations



<table>
  <tr>
   <td><strong>fonctions</strong>
   </td>
   <td><strong>description</strong>
   </td>
  </tr>
  <tr>
   <td>t=Tempo(duree_ms)
   </td>
   <td>t=Tempo(500) créer un objet de temporisation t de durée 500 ms qui se relance indéfiniment. 
<img src="./images/image2.png">
   </td>
  </tr>
  <tr>
   <td>t.fin()
   </td>
   <td>renvoie True lorsque la temporisation est terminée. Pour notre exemple au bout de 500 ms.
   </td>
  </tr>
  <tr>
   <td>t.is_on()
   </td>
   <td>renvoie True si la temporisation est à on.
   </td>
  </tr>
  <tr>
   <td>t.is_off()
   </td>
   <td>renvoie True si la temporisation est à off.
   </td>
  </tr>
  <tr>
   <td>t.set_tempo(duree_ms)
   </td>
   <td>permet de réinitialiser la temporisation avec une nouvelle valeur.
   </td>
  </tr>
  <tr>
   <td>t.reset()
   </td>
   <td>force le redémarrage de la temporisation.
   </td>
  </tr>
</table>