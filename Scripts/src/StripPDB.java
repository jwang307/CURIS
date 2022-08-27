/**
 * Modify PDB to fit GLoSA search requirements
 * arg 1: pass in input file
 * arg 2: "p" for protein, "l" for ligand
 */

import java.io.*;
import java.util.ArrayList;

public class StripPDB {
    public static void main(String[] args) throws IOException {
        if(args.length != 2 || args[0].equalsIgnoreCase("--help")){
            System.out.println( "Usage: Strip PDB File" );
            System.out.println( "          -opts  [pdb file path]" );
            System.out.println( "                 [p for strip to only protein atoms, l for strip to only ligand atoms]" );
            return;
        }

        BufferedReader br = new BufferedReader(new FileReader(args[0]));
        String moleculeType = args[1];
        String match = "ATOM";
        boolean stripAll = false;

        if (moleculeType.equalsIgnoreCase("l")) {
            stripAll = true;
            match = "HETATM";
        } else if (moleculeType.equalsIgnoreCase("p")) {
            stripAll = true;
        }

        String lineIn;
        ArrayList<String> strippedPDB = new ArrayList<>();
        while ((lineIn = br.readLine()) != null) {
            if (!stripAll) {
                if (lineIn.startsWith("ATOM") || lineIn.startsWith("HETATM")) {
                    strippedPDB.add(lineIn);
                }
            } else {
                if (lineIn.startsWith(match)) {
                    strippedPDB.add(lineIn);
                }
            }
        }

        br.close();

        PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(args[0].substring(0, args[0].length() - 4) + "-stripped.pdb")));

        for (String str : strippedPDB) {
            pw.println(str);
        }

        pw.println("TER");
        pw.close();
    }
}
