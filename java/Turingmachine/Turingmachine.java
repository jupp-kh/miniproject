import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.IntStream;

 
class Turingmachine   {
    int zustand;
	int endzustand;
    Map<Integer, Map<Integer, Step>> delta;
    int bandsize;
    int schritte;
    int [] band;
    int kopf ;
    static int anzahlmaschenen = 0;
    
    public Turingmachine(Map<Integer, Map<Integer, Step>> delta,int bandsize,int schrit){
        zustand = 0;
        endzustand = 2;
        band = new int[bandsize];
        kopf = band.length / 2;
        schritte= schrit;
        this.delta = delta;
        for(int i = 0; i < this.band.length; i++){
            band[i] = 2;
        }
    }

    public static Turingmachine createTuringmachine(int seed) {
        int t27pow3 = (int) Math.pow(27, 3);
        int d0i = seed % t27pow3;
        seed = seed / t27pow3;
        int d1i = seed % t27pow3;
        return new Turingmachine(creatDelta(d0i, d1i), 100, 100);
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

    public void run() {
		try {
            for(int i=0 ; i< schritte; i++){
                if(zustand == endzustand) break;
                int zeichen = band[kopf];
                Step step = delta.get(zustand).get(zeichen);
                band[kopf] = step.getWrite() ;
                kopf += step.getMove();
                zustand = step.zustand;
            }
           // if(zustand == 2 && anzahlEins()>= 4) 
        } catch (IndexOutOfBoundsException e) {
            zustand = endzustand;
            for (int i = 0; i < band.length; i++)
                band[i] = 2;
        }
    }
    public int anzahlEins(){
        int einsen = 0;
        for(int i = 0 ; i < band.length; i++)
            if(band[i] == 1) einsen++;
        
        return einsen;
    }
    public static Map<Integer, Map<Integer, Step>>creatDelta(int d0i, int d1i ){

        Map<Integer, Map<Integer, Step>> delta = new HashMap<>();
        
        Map<Integer,Step> d0 = new HashMap<>();
        delta.put(0,d0);
        d0.put(0,new Step(d0i % 27));
        d0i = d0i / 27;
        d0.put(1,new Step(d0i % 27));
        d0i = d0i / 27;
        d0.put(2,new Step(d0i % 27));

        Map<Integer,Step> d1 = new HashMap<>();
        delta.put(1,d1);
        d1.put(0,new Step(d1i % 27));
        d1i = d1i / 27;
        d1.put(1,new Step(d1i % 27));
        d1i = d1i / 27;
        d1.put(2,new Step(d1i % 27));

        return delta;

    }

    public int anzahlEinsen() {
        run();
        return zustand == endzustand ? anzahlEins() : 0;
    }

    public static void main(String[] args) {

        Instant start = Instant.now();

        long count = IntStream.range(0, (int)Math.pow(27, 6))
            .parallel()
            .mapToObj(Turingmachine::createTuringmachine)
            .map(Turingmachine::anzahlEinsen)
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