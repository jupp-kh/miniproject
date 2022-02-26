import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.IntStream;

 
class TuringmachineFast   {
    int zustand = 0;
	int endzustand = 2;
    int[] deltaI = new int[6];
    int bandsize = 100;
    int schritte = 100;
    int [] band;
    int kopf ;
    static int anzahlmaschenen = 0;
    
    public TuringmachineFast(int seed){
        band = new int[bandsize];
        kopf = band.length / 2;
        for(int i = 0; i < this.band.length; i++){
            band[i] = 2;
        }

        int t27pow3 = (int) Math.pow(27, 3);
        int d0i = seed % t27pow3;
        seed = seed / t27pow3;
        int d1i = seed % t27pow3;
        creatDelta(d0i, d1i);
    }


    public String toString(){
        StringBuilder res = new StringBuilder() ;
        int left = 0;
        int right = 0;
        for(int i = 0; i < this.band.length; i++){
            if(this.band[i] != 2){
                left = i-1;
                break;
            }
        }
        for(int i = this.band.length -1 ; i >= 0 ; --i){
            if(this.band[i] != 2){
                right = i+1;
                break;
            }
        }
        for(int i = left ; i <= right ; i++){
            if(i == kopf){
                res.append("q"+ zustand + "[");
                res.append(band[i] == 2 ? "B" : band[i]);
                res.append("]");
            }else{
                res.append(band[i] == 2 ? "B" : band[i]); 
            }
        }
        return res.toString();
    }


    private int getWrite(int step) {
        return step % 3;
    }
    private int getMove(int step) {
        step /= 3;
        return step % 3;
    }
    private int getZustand(int step) {
        step /= 9;
        return step % 3;
    }

    public void run() {
		try {
            for(int i=0 ; i< schritte; i++){
                if(zustand == endzustand) return;
                int zeichen = band[kopf];
                int step = deltaI[zustand * 3 + zeichen];
                band[kopf] = step % 3;
                step /= 3;
                kopf += step % 3;
                step /= 3;
                zustand = step % 3;
            }
           // if(zustand == 2 && anzahlEins()>= 4) 
        } catch (IndexOutOfBoundsException e) {
            zustand = -1;
        }
    }
    public int anzahlEins(){
        int einsen = 0;
        for(int i = 0 ; i < band.length; i++)
            if(band[i] == 1) einsen++;
        
        return einsen;
    }
    private void creatDelta(int d0i, int d1i ){
        deltaI[0] = d0i % 27;
        d0i = d0i / 27;
        deltaI[1] = d0i % 27;
        d0i = d0i / 27;
        deltaI[2] = d0i % 27;

        deltaI[3] = d1i % 27;
        d1i = d1i / 27;
        deltaI[4] = d1i % 27;
        d1i = d1i / 27;
        deltaI[5] = d1i % 27;
    }

    public int anzahlEinsen() {
        run();
        return zustand == endzustand ? anzahlEins() : 0;
    }

    public static void main(String[] args) {

        Instant start = Instant.now();

        long count = IntStream.range(0, (int)Math.pow(27, 6))
            .parallel()
            .mapToObj(TuringmachineFast::new)
            .map(TuringmachineFast::anzahlEinsen)
            .filter(x -> x >= 4)
            .count();

        Instant end = Instant.now();

        System.out.println("Anzahl der TMs, die mind. 8 einsen ausgeben: " + count);
        System.out.println("berechnen dauerte: " + Duration.between(start, end));

        if(true) return;
       
        Map<Integer, Map<Integer, Step>> delta = new HashMap<>();
        Map<Integer,Step> d0 = new HashMap<>();
        delta.put(0,d0);
        d0.put(0,new Step(1,1,1));
        d0.put(1,new Step(2,1,0));
        d0.put(2,new Step(1,0,-1));

        Map<Integer,Step> d1 = new HashMap<>();
        delta.put(1,d1);
        d1.put(0,new Step(1,1,-1));
        d1.put(1,new Step(1,0,1));
        d1.put(2,new Step(0,1,1));
        Turingmachine tm = new Turingmachine(delta, 1000, 1000);
        tm.run();
     
        
        
        //nix gefunden 0-16200-......200000-..........-300000-353100
      /*
        for(int i = 0 ; i<= 27*27*27; i++){
            for(int j = 0; j<= 27*27*27; j++){
                
                Turingmachine tm = new Turingmachine(creatDelta(i, j),100,100);
                tm.run();
                
            }
            if(i%1000 == 0) {
                System.out.println(i);
                System.out.println(anzahlmaschenen);
            }
        } 
      */
    }
}