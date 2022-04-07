var menu;
var play;
class Scene1 extends Phaser.Scene {
    constructor() {
      super("Rue sans temoin");
    }

    

    preload (){ 
      this.load.image("menu", "assets/images/menu.png");
    }

    create(){
  
      menu = this.add.image(640,360, 'menu')
      .setDepth(3)
      .setScrollFactor(0);
    }


    update (){
      this.input.on('pointerdown', function (pointer) {
        menu.destroy();
        play = true;
        
    })
    if(play === true )
      this.scene.start("playGame");
    }
}
