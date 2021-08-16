( function( w )
    {
        w.adam = function( id )
        {
            return new adamClock( id );
        };
        
        var adamClock = function( id )
        {
            this.id = id;
            
            this.def = false;
            
            this.timer = null;
        };
        
        adamClock.prototype = {
            
            _getTime : function( o )
            {
                var h = this._toString( o.getHours() ),
                    m = this._toString( o.getMinutes() ),
                    s = this._toString( o.getSeconds() );
                
                return [
                    h.charAt( 0 ),
                    h.charAt( 1 ),
                    m.charAt( 0 ),
                    m.charAt( 1 ),
                    s.charAt( 0 ),
                    s.charAt( 1 )
                ];
            },
            
            _toString : function( num )
            {
                return ( num > 9  ? num : "0" + num ).toString();
            },
            
            init : function( speed, mode, move )
            {
                speed = speed || 100;
                mode = mode || "modeY";
                move = move || "move";
                
                var _this = this;
                
                Aui("div.time").append("<dl id=" + _this.id + "><dd><span>0</span></dd><dd><span>0</span></dd><dt><span>:</span></dt><dd><span>0</span></dd><dd><span>0</span></dd><dt><span>:</span></dt><dd><span>0</span></dd><dd><span>0</span></dd></dl>");
                
                var oDD = Aui( "#" + _this.id ).find("dd");
                
                _this.timer = setInterval( function()
                {
                    var t = _this._getTime( new Date() ), i;
                    
                    for( i = 5 ; i >= 0; i-= 1)
                    {
                        var thisDD = oDD.eq( i );
                        
                        if( thisDD.find("span").text() == t[ i ] && _this.def ) break;
                        
                        console.log( thisDD )
                        thisDD.addClass( move + " " + mode ).find("span").text( t[ i ] ); //.next().text( t[ i ] )
                        
                        ( function( o )
                        {
                            setTimeout(function()
                            {
                                o.removeClass( move + " " + mode );
                            }, speed + 10 );
                            
                        })( thisDD )
                        
                    };
                    
                    _this.def = true;
                    
                }, 1000 );
                
                return this;
            }
            
        };
    })( window );
    
    Aui.ready( function()
    {
        if( /ie/g.test( Aui.browser() ) )
        {
            Aui("body").html("Adam CSS 3.0 effect，支持非IE浏览器。你懂的！")
                       .setStyle(
                       {
                           "color" : "#fff",
                           "text-align" : "center",
                        "font-size" : "50px",
                        "font-weight" : "bolder",
                        "line-height" : "500px"
                       });
        }
        else
        {
            adam("demo1").init( 600, "move", "modeX" );
        };
    
    });