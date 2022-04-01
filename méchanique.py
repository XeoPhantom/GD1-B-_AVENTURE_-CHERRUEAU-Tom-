<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" /><title>Aventure</title>
        <script src="//cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.js"></script>
        <style type="text/css"> body { margin: 0; }</style>
    </head>

    <body>
        <script type="text/javascript">

            /*var bullets;
            var ship;
            var speed;
            var stats;
            var lastFired = 0;
            var isDown = false;
            var mouseX = 0;
            var mouseY = 0;
            var cursors;*/

            

            class Scene1 extends Phaser.Scene {
                constructor(){
                    super("Scene1");
                }

                preload () {
                    this.load.image('ship', 'assets/sprites/star.png');
                    this.load.image('bullet1', 'assets/sprites/bomb.png');
                    this.load.image('sky', 'assets/sky.png');
                }

                create () {
                    this.ship = this.add.sprite(400, 300, 'ship').setDepth(1);
                    this.cursors = this.input.keyboard.createCursorKeys();
                    this.speed = Phaser.Math.GetSpeed(300, 1);
                    this.lastFired = 0;
                    this.isDown = false;
                    this.mouseX=0;
                    this.mouseY=0;
                    this.add.image(400, 300, 'sky');
                    
                    var Bullet = new Phaser.Class({

                        Extends: Phaser.GameObjects.Image,
                        initialize:

                        function Bullet (scene) {
                            Phaser.GameObjects.Image.call(this, scene, 0, 0, 'bullet1');

                            this.incX = 0;
                            this.incY = 0;
                            this.lifespan = 0;

                            this.speed = Phaser.Math.GetSpeed(600, 1);
                        },

                        fire: function (ship, x, y) {
                            this.setActive(true);
                            this.setVisible(true);

                            //  Bullets fire from the middle of the screen to the given x/y
                            this.setPosition(ship.x, ship.y);

                            var angle = Phaser.Math.Angle.Between(x, y, ship.x, ship.y);

                            this.setRotation(angle);

                            this.incX = Math.cos(angle);
                            this.incY = Math.sin(angle);

                            this.lifespan = 1000;
                        },

                        update: function (time, delta) {
                            this.lifespan -= delta;

                            this.x -= this.incX * (this.speed * delta);
                            this.y -= this.incY * (this.speed * delta);

                            if (this.lifespan <= 0) {
                                this.setActive(false);
                                this.setVisible(false);
                            }
                        }

                    });

                    this.bullets = this.add.group({
                        classType: Bullet,
                        maxSize: 50,
                        runChildUpdate: true
                    });                    

                    this.input.on('pointerdown', pointer =>  {

                        this.isDown = true;
                        this.mouseX = pointer.x;
                        this.mouseY = pointer.y;

                    });

                    this.input.on('pointermove', pointer =>  {

                        this.mouseX = pointer.x;
                        this.mouseY = pointer.y;

                    });

                    this.input.on('pointerup', pointer =>  {

                        this.isDown = false;

                    });

                }

                update (time, delta) {
                    if (this.cursors.left.isDown) {
                        //this.ship.x -= this.speed * delta;
                        this.scene.start('myScene');
                    }
                    if (this.cursors.right.isDown) {
                        this.ship.x += this.speed * delta;
                    }
                    if (this.cursors.down.isDown) {
                        this.ship.y += this.speed * delta;
                    }
                    if (this.cursors.up.isDown) {
                        this.ship.y -= this.speed * delta;
                    }

                    if (this.cursors)

                    if (this.isDown && time > this.lastFired) {
                        this.bullet = this.bullets.get();

                        if (this.bullet) {
                            this.bullet.fire(this.ship, this.mouseX, this.mouseY);

                            this.lastFired = time + 500;
                        }
                    }

                    this.ship.setRotation(Phaser.Math.Angle.Between(this.mouseX, this.mouseY, this.ship.x, this.ship.y) - Math.PI / 2);

                }
            }

            class MyScene extends Phaser.Scene {
               
                preload(){
                    this.load.image('sky', 'assets/sky.png');
                    this.load.image('ground', 'assets/platform.png');
                    this.load.image('star', 'assets/star.png');
                    this.load.image('bomb', 'assets/bomb.png');
                    this.load.spritesheet('dude', 'assets/dude.png', { frameWidth: 32, frameHeight: 48 });
                }
                create(){
                    this.gameOver = false;
                    //  A simple background for our game
                    this.add.image(400, 300, 'sky');

                    //  The platforms group contains the ground and the 2 ledges we can jump on
                    this.platforms = this.physics.add.staticGroup();

                    //  Here we create the ground.
                    //  Scale it to fit the width of the game (the original sprite is 400x32 in size)
                    this.platforms.create(400, 568, 'ground').setScale(2).refreshBody();

                    //  Now let's create some ledges
                    this.platforms.create(600, 400, 'ground');
                    this.platforms.create(50, 250, 'ground');
                    this.platforms.create(750, 220, 'ground');

                    // The player and its settings
                    this.player = this.physics.add.sprite(100, 450, 'dude');

                    //  Player physics properties. Give the little guy a slight bounce.
                    this.player.setBounce(0.2);
                    this.player.setCollideWorldBounds(true);

                    //  Our player animations, turning, walking left and walking right.
                    this.anims.create({
                        key: 'left',
                        frames: this.anims.generateFrameNumbers('dude', { start: 0, end: 3 }),
                        frameRate: 10,
                        repeat: -1
                    });

                    this.anims.create({
                        key: 'turn',
                        frames: [ { key: 'dude', frame: 4 } ],
                        frameRate: 20
                    });

                    this.anims.create({
                        key: 'right',
                        frames: this.anims.generateFrameNumbers('dude', { start: 5, end: 8 }),
                        frameRate: 10,
                        repeat: -1
                    });

                    //  Input Events
                    this.cursors = this.input.keyboard.createCursorKeys();

                    //  Some stars to collect, 12 in total, evenly spaced 70 pixels apart along the x axis
                    this.stars = this.physics.add.group({
                        key: 'star',
                        repeat: 11,
                        setXY: { x: 12, y: 0, stepX: 70 }
                    });

                    this.stars.children.iterate(function (child) {

                        //  Give each star a slightly different bounce
                        child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));

                    });

                    this.bombs = this.physics.add.group();

                    //  The score
                    this.scoreText = this.add.text(16, 16, 'score: 0', { fontSize: '32px', fill: '#000' });

                    //  Collide the player and the stars with the platforms
                    this.physics.add.collider(this.player, this.platforms);
                    this.physics.add.collider(this.stars, this.platforms);
                    this.physics.add.collider(this.bombs, this.platforms);

                    //  Checks to see if the player overlaps with any of the stars, if he does call the collectStar function
                    this.physics.add.overlap(this.player, this.stars, this.collectStar, null, this);

                    this.physics.add.collider(this.player, this.bombs, hitBomb, null, this);
                }
                
                update(){
                    if (this.gameOver)
                    {
                        return;
                    }

                    if (this.cursors.left.isDown)
                    {
                        this.player.setVelocityX(-160);

                        this.player.anims.play('left', true);
                    }
                    else if (this.cursors.right.isDown)
                    {
                        this.player.setVelocityX(160);

                        this.player.anims.play('right', true);
                    }
                    else
                    {
                        this.player.setVelocityX(0);

                        this.player.anims.play('turn');
                    }

                    if (this.cursors.up.isDown && this.player.body.touching.down)
                    {
                        this.player.setVelocityY(-330);
                    }
                }

                collectStar (player, star)
                {
                    star.disableBody(true, true);

                    //  Add and update the score
                    player.scene.score += 10;
                    player.scene.scoreText.setText('Score: ' + player.scene.score);

                    if (player.scene.stars.countActive(true) === 0)
                    {
                        //  A new batch of stars to collect
                        player.scene.stars.children.iterate(function (child) {

                            child.enableBody(true, child.x, 0, true, true);

                        });

                        var x = (player.x < 400) ? Phaser.Math.Between(400, 800) : Phaser.Math.Between(0, 400);

                        var bomb = this.bombs.create(x, 16, 'bomb');
                        bomb.setBounce(1);
                        bomb.setCollideWorldBounds(true);
                        bomb.setVelocity(Phaser.Math.Between(-200, 200), 20);

                    }
                }

            }

            var config = {
                type: Phaser.WEBGL,
                width: 800,
                height: 600,
                physics: {
                    default: 'arcade',
                    arcade: {
                        gravity: { y: 300 },
                        debug: false
                    }
                },
                backgroundColor: '#2d2d2d',
                parent: 'phaser-example',
                scene: Scene1
            };

            function hitBomb (player, bomb)
            {
                this.physics.pause();

                player.setTint(0xff0000);

                player.anims.play('turn');

                player.scene.gameOver = true;
            }

            var game = new Phaser.Game(config);
        </script>
    </body>
</html>