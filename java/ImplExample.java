import com.ib.client.*;

public class ImplExample {

	public static void main(String[] args) {
		EWrapperImpl wrapper = new EWrapperImpl();
		
		EClientSocket client = wrapper.getClient();
		EReaderSignal signal = wrapper.getSignal();
        
		client.eConnect("127.0.0.1", 7497, 0);

		EReader reader = new EReader(client, signal);   
		reader.start();

		new Thread(() -> {
		    while (client.isConnected()) {
		        signal.waitForSignal();
		        try {
		            reader.processMsgs();
		        } catch (Exception e) {
		            System.out.println("Exception: "+e.getMessage());
		        }
		    }
		}).start();

        Contract contract = new Contract();
        contract.conid(265598);
        contract.exchange("SMART");

        Contract contract2 = new Contract();
        contract2.conid(8314);
        contract2.exchange("SMART");

        client.reqMktData(wrapper.getCurrentOrderId(), contract, null, false, false, null);
        client.reqMktData(wrapper.getCurrentOrderId(), contract2, null, false, false, null);
	}
}