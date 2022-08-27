import java.io.*;
import java.text.DecimalFormat;


public class GetTopTemplatesDebug{
    public static void main( String[] args ) throws IOException{
        if( args.length == 0 || args.length != 4 || args[0].equalsIgnoreCase( "--help" ) ){
            System.out.println( "Usage: GetTopTemplates" );
            System.out.println( "             -opts [result file: score.txt]" );
            System.out.println( "                   [top N]" );
            System.out.println( "                   [cutoff GA-score]" );
            System.out.println( "                   [output file]" );

            return;
        }


        String mResults = args[0];
        int mTopN = Integer.parseInt( args[1] );
        double mCutoffGAScore = Double.parseDouble( args[2] );
        String mOutput = args[3];



        FileInputStream result_stream;
        BufferedReader result_reader;
        String result_line;

        DataOutputStream out;


        String [] array;



        try{
            int num_data = 0;

            result_stream = new FileInputStream( new File( mResults ) );
            result_reader = new BufferedReader( new InputStreamReader( result_stream ) );

            while( ( result_line = result_reader.readLine()) != null ){
                num_data++;
            }

            result_reader.close();
            result_stream.close();


            System.out.println(num_data);
            double [] aGAScore = new double[num_data];
            String [] aContext = new String[num_data];

            result_stream = new FileInputStream( new File( mResults ) );
            result_reader = new BufferedReader( new InputStreamReader( result_stream ) );

            int index = -1;

            while( ( result_line = result_reader.readLine()) != null ){
                index++;
                array = result_line.split( "\t" );

                aGAScore[index] = Double.parseDouble( array[1] );
                aContext[index] = result_line;
            }

            result_reader.close();
            result_stream.close();




            quicksortDescending( aContext, aGAScore, 0, num_data - 1 );


            out = new DataOutputStream( new FileOutputStream( new File( mOutput ) ) );

            for( int i = 0 ; i < mTopN ; i++ ){
                if( aGAScore[i] >= mCutoffGAScore )
                    out.writeBytes( aContext[i] + "\n" );
            }

            out.close();
        }
        catch( Exception exception ){
            exception.printStackTrace();
        }
    }






    static void quicksortDescending( String context_array[], double score_array[], int low, int high ){
        int i = low;
        int j = high;
        double y = 0;
        String context;

        double z = score_array[(low + high) / 2];

        do{
            while( score_array[i] > z ) i++;

            while( score_array[j] < z ) j--;

            if( i <= j ) {
                // swap two elements
                y = score_array[i];
                score_array[i] = score_array[j];
                score_array[j] = y;

                context = context_array[i];
                context_array[i] = context_array[j];
                context_array[j] = context;

                i++;
                j--;
            }
        }while( i <= j );

        if( low < j )
            quicksortDescending( context_array, score_array, low, j );

        if( i < high )
            quicksortDescending( context_array, score_array, i, high );
    }
}







